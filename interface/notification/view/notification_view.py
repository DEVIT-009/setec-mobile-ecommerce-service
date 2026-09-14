from rest_framework.views import APIView
from rest_framework.request import Request

from application.notification.factory.notification_service_factory import notification_service_factory
from shared.responseutils.response_handler import ResponseHandler
from shared.metadata_handler.request_header_utillity import metadata_handler
from shared.pagination.api_paging import ApiPaging


class NotificationListView(APIView):
    @metadata_handler(required_user_id=True)
    def get(self, request: Request, metadata=None):
        paging = ApiPaging.from_request(request)
        service = notification_service_factory()
        result = service.list(metadata.user_id, page=paging['page'], page_size=paging['page_size'])
        return ResponseHandler.api_list(result['items'], paging['page'], paging['page_size'], result['total'])


class NotificationUnreadCountView(APIView):
    @metadata_handler(required_user_id=True)
    def get(self, request: Request, metadata=None):
        service = notification_service_factory()
        count = service.unread_count(metadata.user_id)
        return ResponseHandler.api_success({"unread_count": count})


class NotificationReadAllView(APIView):
    @metadata_handler(required_user_id=True)
    def post(self, request: Request, metadata=None):
        service = notification_service_factory()
        service.mark_all_read(metadata.user_id)
        return ResponseHandler.api_no_content()


class NotificationDetailView(APIView):
    @metadata_handler(required_user_id=True)
    def delete(self, request: Request, notification_id=None, metadata=None):
        service = notification_service_factory()
        service.delete(str(notification_id), metadata.user_id)
        return ResponseHandler.api_no_content()


class NotificationReadView(APIView):
    @metadata_handler(required_user_id=True)
    def post(self, request: Request, notification_id=None, metadata=None):
        service = notification_service_factory()
        return ResponseHandler.api_success(service.mark_read(str(notification_id), metadata.user_id))
