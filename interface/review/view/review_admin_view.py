from rest_framework.views import APIView
from rest_framework.request import Request

from application.review.factory.review_service_factory import review_service_factory
from interface.review.serializer.request.review_request import AdminUpdateReviewStatusRequest
from shared.responseutils.response_handler import ResponseHandler
from shared.metadata_handler.request_header_utillity import metadata_handler
from shared.permission_handler import require_roles
from shared.pagination.api_paging import ApiPaging



class AdminReviewListView(APIView):
    """
    GET /api/v1/admin/reviews/  — list all non-deleted reviews (all statuses).
    """

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def get(self, request: Request, metadata=None):
        paging = ApiPaging.from_request(request)
        filters = {
            'product_id': request.query_params.get('product_id'),
            'user_id': request.query_params.get('user_id'),
            'status': request.query_params.get('status'),
        }
        service = review_service_factory()
        result = service.list_admin(filters=filters, page=paging['page'], page_size=paging['page_size'])
        return ResponseHandler.api_list(result['items'], paging['page'], paging['page_size'], result['total'])


class AdminReviewDetailView(APIView):
    """
    GET    /api/v1/admin/reviews/<uuid:review_id>/
    PATCH  /api/v1/admin/reviews/<uuid:review_id>/  — update status (approve/reject)
    DELETE /api/v1/admin/reviews/<uuid:review_id>/  — soft-delete
    """

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def get(self, request: Request, review_id=None, metadata=None):
        service = review_service_factory()
        return ResponseHandler.api_success(service.get_admin(str(review_id)))

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def patch(self, request: Request, review_id=None, metadata=None):
        serializer = AdminUpdateReviewStatusRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = review_service_factory()
        return ResponseHandler.api_success(service.update_admin(str(review_id), serializer.validated_data, actor_id=metadata.user_id))


    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def delete(self, request: Request, review_id=None, metadata=None):
        service = review_service_factory()
        service.delete_admin(str(review_id), actor_id=metadata.user_id)
        return ResponseHandler.api_no_content()
