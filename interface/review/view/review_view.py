from rest_framework.views import APIView
from rest_framework.request import Request

from application.review.factory.review_service_factory import review_service_factory
from interface.review.serializer.mapper.review_controller_mapper import ReviewControllerMapper
from interface.review.serializer.request.review_request import (
    CreateReviewRequest,
    UpdateReviewRequest,
    CreateReviewSerializer,
    UpdateReviewSerializer,
)
from shared.responseutils.response_handler import ResponseHandler
from shared.metadata_handler.request_header_utillity import metadata_handler
from shared.pagination.api_paging import ApiPaging


class ProductReviewCreateView(APIView):
    @metadata_handler(required_user_id=True)
    def post(self, request: Request, product_id=None, metadata=None):
        serializer = CreateReviewRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = review_service_factory()
        payload = ReviewControllerMapper.from_create_request(serializer.validated_data, product_id=product_id)
        data = service.create(metadata.user_id, payload)
        return ResponseHandler.api_created(data)


class ReviewListView(APIView):
    """
    GET /api/v1/reviews/  — list published customer reviews, filterable by product_id
    """
    @metadata_handler(required_user_id=False)
    def get(self, request: Request, metadata=None):
        paging = ApiPaging.from_request(request)
        product_id = request.query_params.get('product_id')
        service = review_service_factory()
        result = service.list_public(
            product_id=product_id,
            page=paging['page'],
            page_size=paging['page_size'],
        )
        return ResponseHandler.api_list(result['items'], paging['page'], paging['page_size'], result['total'])


class ReviewDetailView(APIView):
    @metadata_handler(required_user_id=False)
    def get(self, request: Request, review_id=None, metadata=None):
        service = review_service_factory()
        return ResponseHandler.api_success(service.get_public(str(review_id)))

    @metadata_handler(required_user_id=True)
    def patch(self, request: Request, review_id=None, metadata=None):
        serializer = UpdateReviewRequest(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        service = review_service_factory()
        return ResponseHandler.api_success(service.update(metadata.user_id, str(review_id), serializer.validated_data))

    @metadata_handler(required_user_id=True)
    def delete(self, request: Request, review_id=None, metadata=None):
        service = review_service_factory()
        service.delete(metadata.user_id, str(review_id))
        return ResponseHandler.api_no_content()


class UserReviewListView(APIView):
    @metadata_handler(required_user_id=True)
    def get(self, request: Request, metadata=None):
        paging = ApiPaging.from_request(request)
        service = review_service_factory()
        result = service.list_by_user(metadata.user_id, page=paging['page'], page_size=paging['page_size'])
        return ResponseHandler.api_list(result['items'], paging['page'], paging['page_size'], result['total'])

