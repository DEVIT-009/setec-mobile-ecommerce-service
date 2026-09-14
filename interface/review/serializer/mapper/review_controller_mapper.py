from typing import Dict, Any, List
from dataclasses import asdict
from domain.review.entity.review import Review
from interface.review.serializer.response.review_response import ReviewResponse


class ReviewControllerMapper:

    @staticmethod
    def from_create_request(validated_data: Dict[str, Any], product_id: str = None) -> Dict[str, Any]:
        return {
            "product_id": str(product_id) if product_id else str(validated_data.get("product_id")),
            "rating": validated_data["rating"],
            "title": validated_data.get("title"),
            "body": validated_data.get("body"),
            "order_item_id": str(validated_data["order_item_id"]) if validated_data.get("order_item_id") else None,
        }

    @staticmethod
    def to_response(review: Review) -> Dict[str, Any]:
        response_dto = ReviewResponse(
            id=str(review.id) if review.id else "",
            product_id=str(review.product_id) if review.product_id else "",
            user_id=str(review.user_id) if review.user_id else "",
            order_item_id=str(review.order_item_id) if review.order_item_id else None,
            rating=review.rating,
            title=review.title,
            body=review.body,
            status=review.status,
            created_at=review.created_at.isoformat() if review.created_at else None,
        )
        return asdict(response_dto)

    @staticmethod
    def to_list_response(reviews: List[Review]) -> List[Dict[str, Any]]:
        return [ReviewControllerMapper.to_response(r) for r in reviews]

