from rest_framework.views import APIView
from rest_framework.request import Request

from application.support_ticket.factory.support_ticket_service_factory import support_ticket_service_factory
from interface.support_ticket.serializer.request.support_ticket_request import (
    CreateTicketRequest,
    UpdateTicketRequest,
    AddTicketMessageRequest,
    CreateTicketSerializer,
    UpdateTicketSerializer,
    AddTicketMessageSerializer,
)
from shared.responseutils.response_handler import ResponseHandler
from shared.metadata_handler.request_header_utillity import metadata_handler
from shared.pagination.api_paging import ApiPaging


class SupportTicketListView(APIView):
    @metadata_handler(required_user_id=True)
    def get(self, request: Request, metadata=None):
        paging = ApiPaging.from_request(request)
        service = support_ticket_service_factory()
        result = service.list(metadata.user_id, page=paging['page'], page_size=paging['page_size'])
        return ResponseHandler.api_list(result['items'], paging['page'], paging['page_size'], result['total'])

    @metadata_handler(required_user_id=True)
    def post(self, request: Request, metadata=None):
        serializer = CreateTicketRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = support_ticket_service_factory()
        data = serializer.validated_data.copy()
        if data.get('order_id'):
            data['order_id'] = str(data['order_id'])
        return ResponseHandler.api_created(service.create(metadata.user_id, data))


class SupportTicketDetailView(APIView):
    @metadata_handler(required_user_id=True)
    def get(self, request: Request, ticket_id=None, metadata=None):
        service = support_ticket_service_factory()
        return ResponseHandler.api_success(service.get(str(ticket_id), metadata.user_id))

    @metadata_handler(required_user_id=True)
    def patch(self, request: Request, ticket_id=None, metadata=None):
        serializer = UpdateTicketRequest(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        service = support_ticket_service_factory()
        return ResponseHandler.api_success(service.update(str(ticket_id), metadata.user_id, serializer.validated_data))


class SupportTicketMessageListView(APIView):
    @metadata_handler(required_user_id=True)
    def get(self, request: Request, ticket_id=None, metadata=None):
        paging = ApiPaging.from_request(request)
        service = support_ticket_service_factory()
        result = service.list_messages(str(ticket_id), metadata.user_id, page=paging['page'], page_size=paging['page_size'])
        return ResponseHandler.api_list(result['items'], paging['page'], paging['page_size'], result['total'])

    @metadata_handler(required_user_id=True)
    def post(self, request: Request, ticket_id=None, metadata=None):
        serializer = AddTicketMessageRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = support_ticket_service_factory()
        return ResponseHandler.api_created(service.add_message(str(ticket_id), metadata.user_id, serializer.validated_data['body']))

