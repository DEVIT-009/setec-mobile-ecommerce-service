from rest_framework.views import APIView
from rest_framework.request import Request

from application.support_ticket.factory.support_ticket_service_factory import support_ticket_service_factory
from interface.support_ticket.serializer.request.support_ticket_request import (
    AdminUpdateTicketRequest,
    AdminReplyTicketRequest,
    AdminUpdateTicketSerializer,
    AdminReplyTicketSerializer,
    TICKET_STATUS_CHOICES,
    TICKET_PRIORITY_CHOICES,
)
from shared.responseutils.response_handler import ResponseHandler
from shared.metadata_handler.request_header_utillity import metadata_handler
from shared.permission_handler import require_roles
from shared.pagination.api_paging import ApiPaging



class AdminSupportTicketListView(APIView):
    """
    GET /api/v1/admin/support/tickets/  — list all non-deleted support tickets.
    """

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def get(self, request: Request, metadata=None):
        paging = ApiPaging.from_request(request)
        filters = {
            'status': request.query_params.get('status'),
            'priority': request.query_params.get('priority'),
            'user_id': request.query_params.get('user_id'),
        }
        service = support_ticket_service_factory()
        result = service.list_admin(filters=filters, page=paging['page'], page_size=paging['page_size'])
        return ResponseHandler.api_list(result['items'], paging['page'], paging['page_size'], result['total'])


class AdminSupportTicketDetailView(APIView):
    """
    GET   /api/v1/admin/support/tickets/<uuid:ticket_id>/
    PATCH /api/v1/admin/support/tickets/<uuid:ticket_id>/  — update status/priority
    """

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def get(self, request: Request, ticket_id=None, metadata=None):
        service = support_ticket_service_factory()
        return ResponseHandler.api_success(service.get_admin(str(ticket_id)))

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def patch(self, request: Request, ticket_id=None, metadata=None):
        serializer = AdminUpdateTicketRequest(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data.copy()
        if data.get('assigned_to'):
            data['assigned_to'] = str(data['assigned_to'])
        service = support_ticket_service_factory()
        return ResponseHandler.api_success(service.update_admin(str(ticket_id), data, actor_id=metadata.user_id))


class AdminSupportTicketReplyView(APIView):
    """
    POST /api/v1/admin/support/tickets/<uuid:ticket_id>/messages/
    """

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def post(self, request: Request, ticket_id=None, metadata=None):
        serializer = AdminReplyTicketRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = support_ticket_service_factory()
        result = service.add_message(str(ticket_id), metadata.user_id, serializer.validated_data['body'])
        return ResponseHandler.api_created(result)

