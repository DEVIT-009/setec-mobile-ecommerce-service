from typing import Optional
from domain.review.entity.review import Review as DomainReview
from infrastructure.persistence.models.review_model import Review as ProductReviewModel


class ReviewPersistenceMapper:

    @staticmethod
    def from_entity(entity: Optional[ProductReviewModel]) -> Optional[DomainReview]:
        if entity is None:
            return None
        return DomainReview(
            id=str(entity.id),
            user_id=str(entity.user_id) if entity.user_id else None,
            product_id=str(entity.product_id) if entity.product_id else None,
            order_item_id=str(entity.order_item_id) if entity.order_item_id else None,
            rating=entity.rating,
            title=entity.title,
            body=entity.body,
            status=entity.status,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            deleted_at=entity.deleted_at,
        )

    @staticmethod
    def to_model(domain: DomainReview, model_instance: Optional[ProductReviewModel] = None) -> ProductReviewModel:
        model = model_instance or ProductReviewModel()
        if domain.user_id:
            model.user_id = domain.user_id
        if domain.product_id:
            model.product_id = domain.product_id
        if domain.order_item_id:
            model.order_item_id = domain.order_item_id
        model.rating = domain.rating
        model.title = domain.title
        model.body = domain.body
        model.status = domain.status
        model.deleted_at = domain.deleted_at
        return model
