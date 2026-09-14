from rest_framework.views import APIView
from rest_framework.request import Request

from application.notification.factory.notification_service_factory import notification_service_factory
from interface.notification.serializer.request.notification_request import (
    AdminSendNotificationRequest,
    AdminSendNotificationSerializer,
    NOTIFICATION_TYPE_CHOICES,
)
from shared.responseutils.response_handler import ResponseHandler
from shared.metadata_handler.request_header_utillity import metadata_handler
from shared.permission_handler import require_roles
from shared.pagination.api_paging import ApiPaging


class AdminNotificationListView(APIView):
    """
    GET  /api/v1/admin/notifications/  — list all non-deleted notifications.
    POST /api/v1/admin/notifications/  — send a notification to a specific user.
    """

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def get(self, request: Request, metadata=None):
        paging = ApiPaging.from_request(request)
        filters = {
            'user_id': request.query_params.get('user_id'),
            'type': request.query_params.get('type'),
        }
        service = notification_service_factory()
        result = service.list_admin(filters=filters, page=paging['page'], page_size=paging['page_size'])
        return ResponseHandler.api_list(result['items'], paging['page'], paging['page_size'], result['total'])

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def post(self, request: Request, metadata=None):
        serializer = AdminSendNotificationRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = notification_service_factory()
        data = serializer.validated_data.copy()
        data['user_id'] = str(data['user_id'])
        result = service.create_admin_notification(data)
        return ResponseHandler.api_created(result)

