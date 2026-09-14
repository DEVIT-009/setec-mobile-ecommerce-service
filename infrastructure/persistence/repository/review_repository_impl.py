from typing import Optional, List, Tuple
from django.utils import timezone
from domain.review.ports.review_repository import ReviewRepositoryInterface
from domain.review.entity.review import Review
from domain.review.exception.review_exception import ReviewException
from infrastructure.persistence.mapper.review_persistence_mapper import ReviewPersistenceMapper
from infrastructure.persistence.models.review_model import ProductReview as ProductReviewModel
from infrastructure.persistence.models.product_model import Product as ProductModel
from infrastructure.persistence.models.order_model import OrderItem as OrderItemModel


class ReviewRepositoryInterfaceImpl(ReviewRepositoryInterface):

    def create(self, review: Review, user_id: str) -> Review:
        # 1. Validate product exists and is not deleted
        if not review.product_id:
            raise ReviewException.product_not_found()

        try:
            product_exists = ProductModel.objects.filter(
                id=review.product_id, deleted_at__isnull=True
            ).exists()
        except Exception:
            raise ReviewException.product_not_found()

        if not product_exists:
            raise ReviewException.product_not_found()

        # 2. Validate order_item_id if provided
        if review.order_item_id:
            try:
                order_item = OrderItemModel.objects.filter(
                    id=review.order_item_id, deleted_at__isnull=True
                ).select_related('order').first()
            except Exception:
                raise ReviewException.order_item_not_found()

            if not order_item:
                raise ReviewException.order_item_not_found()

            if str(order_item.order.user_id) != str(user_id):
                raise ReviewException.invalid_order_item("Order item does not belong to the current user")

            if str(order_item.product_id) != str(review.product_id):
                raise ReviewException.invalid_order_item("Order item does not belong to this product")

            exists = ProductReviewModel.objects.filter(
                user_id=user_id, order_item_id=review.order_item_id, deleted_at__isnull=True
            ).exists()
            if exists:
                raise ReviewException.duplicate_review()

        model = ReviewPersistenceMapper.to_model(review)
        model.user_id = user_id
        model.save()
        return ReviewPersistenceMapper.from_entity(model)

    def get_by_id(self, review_id: str) -> Optional[Review]:
        model = ProductReviewModel.objects.filter(id=review_id, deleted_at__isnull=True).first()
        if not model:
            return None
        return ReviewPersistenceMapper.from_entity(model)

    def save(self, review: Review) -> Review:
        db_instance = ProductReviewModel.objects.filter(pk=review.id).first() if review.id else None
        db_instance = ReviewPersistenceMapper.to_model(review, db_instance)
        db_instance.save()
        return ReviewPersistenceMapper.from_entity(db_instance)

    def soft_delete(self, review_id: str, user_id: str) -> None:
        model = ProductReviewModel.objects.filter(id=review_id, user_id=user_id, deleted_at__isnull=True).first()
        if not model:
            raise ReviewException.not_found()
        model.deleted_at = timezone.now()
        model.save()

    def list_published(self, product_id: Optional[str] = None, page: int = 1, page_size: int = 20) -> Tuple[List[Review], int]:
        qs = ProductReviewModel.objects.filter(status='published', deleted_at__isnull=True).order_by('-created_at')
        if product_id:
            qs = qs.filter(product_id=product_id)
        total = qs.count()
        offset = (page - 1) * page_size
        models = list(qs[offset:offset + page_size])
        return [ReviewPersistenceMapper.from_entity(m) for m in models if m is not None], total

    def list_by_product(self, product_id: str, page: int, page_size: int) -> Tuple[List[Review], int]:
        return self.list_published(product_id=product_id, page=page, page_size=page_size)

    def list_by_user(self, user_id: str, page: int, page_size: int) -> Tuple[List[Review], int]:
        qs = ProductReviewModel.objects.filter(user_id=user_id, deleted_at__isnull=True).order_by('-created_at')
        total = qs.count()
        offset = (page - 1) * page_size
        models = list(qs[offset:offset + page_size])
        return [ReviewPersistenceMapper.from_entity(m) for m in models if m is not None], total
