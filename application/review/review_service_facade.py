from typing import Dict, Any
from domain.review.ports.review_repository import ReviewRepositoryInterface
from domain.review.service.review_service import ReviewServiceInterface
from domain.review.entity.review import Review
from domain.review.exception.review_exception import ReviewException
from interface.review.serializer.mapper.review_controller_mapper import ReviewControllerMapper


class ReviewServiceFacade(ReviewServiceInterface):

    def __init__(self, repo: ReviewRepositoryInterface):
        self.repo = repo

    def create(self, user_id: str, data: dict) -> Dict[str, Any]:
        product_id = data.get('product_id')
        if not product_id:
            raise ReviewException.product_not_found()

        rating = data.get('rating')
        if rating is None or not (1 <= int(rating) <= 5):
            raise ReviewException.invalid_rating()

        order_item_id = data.get('order_item_id')
        if order_item_id in ('', 'null', 'None'):
            order_item_id = None

        review = Review(
            product_id=str(product_id),
            order_item_id=str(order_item_id) if order_item_id else None,
            rating=int(rating),
            title=data.get('title'),
            body=data.get('body'),
            status='published',
        )
        saved = self.repo.create(review, user_id)
        return ReviewControllerMapper.to_response(saved)

    def update(self, user_id: str, review_id: str, data: dict) -> Dict[str, Any]:
        review = self.repo.get_by_id(review_id)
        if not review or review.user_id != user_id:
            raise ReviewException.not_found()

        if 'rating' in data:
            r = int(data['rating'])
            if not (1 <= r <= 5):
                raise ReviewException.invalid_rating()
            review.rating = r
        if 'title' in data:
            review.title = data['title']
        if 'body' in data:
            review.body = data['body']

        saved = self.repo.save(review)
        return ReviewControllerMapper.to_response(saved)

    def delete(self, user_id: str, review_id: str) -> None:
        self.repo.soft_delete(review_id, user_id)

    def list_by_user(self, user_id: str, page: int, page_size: int) -> Dict[str, Any]:
        reviews, total = self.repo.list_by_user(user_id, page, page_size)
        return {
            "items": ReviewControllerMapper.to_list_response(reviews),
            "total": total,
        }

    def list_admin(self, filters: dict, page: int, page_size: int) -> Dict[str, Any]:
        from infrastructure.persistence.models.review_model import Review as ProductReview
        qs = ProductReview.objects.filter(deleted_at__isnull=True).order_by('-created_at')
        if filters.get('status'):
            qs = qs.filter(status=filters['status'])
        if filters.get('product_id'):
            qs = qs.filter(product_id=filters['product_id'])
        total = qs.count()
        offset = (page - 1) * page_size
        models = list(qs[offset:offset + page_size])
        return {
            "items": [
                {
                    "id": str(r.id), "product_id": str(r.product_id), "user_id": str(r.user_id),
                    "rating": r.rating, "title": r.title, "body": r.body, "status": r.status,
                    "created_at": r.created_at.isoformat() if r.created_at else None,
                }
                for r in models
            ],
            "total": total,
        }

    def set_status(self, review_id: str, status: str) -> Dict[str, Any]:
        review = self.repo.get_by_id(review_id)
        if not review:
            raise ReviewException.not_found()
        review.status = status
        saved = self.repo.save(review)
        return ReviewControllerMapper.to_response(saved)

    def get_admin(self, review_id: str) -> Dict[str, Any]:
        review = self.repo.get_by_id(review_id)
        if not review:
            raise ReviewException.not_found()
        return ReviewControllerMapper.to_response(review)

    def update_admin(self, review_id: str, data: dict, actor_id: str = None) -> Dict[str, Any]:
        status = data.get('status')
        if status:
            return self.set_status(review_id, status)
        return self.get_admin(review_id)

    def delete_admin(self, review_id: str, actor_id: str = None) -> None:
        review = self.repo.get_by_id(review_id)
        if not review:
            raise ReviewException.not_found()
        self.repo.soft_delete(review_id, review.user_id)

    def list_public(self, product_id: str = None, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        reviews, total = self.repo.list_published(product_id=product_id, page=page, page_size=page_size)
        return {
            "items": ReviewControllerMapper.to_list_response(reviews),
            "total": total,
        }

    def get_public(self, review_id: str) -> Dict[str, Any]:
        review = self.repo.get_by_id(review_id)
        if not review or review.status != 'published':
            raise ReviewException.not_found()
        return ReviewControllerMapper.to_response(review)

