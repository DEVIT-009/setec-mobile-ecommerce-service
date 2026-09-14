from rest_framework.views import APIView
from rest_framework.request import Request

from application.conversation.factory.conversation_service_factory import conversation_service_factory
from interface.conversation.serializer.request.conversation_request import (
    CreateConversationRequest,
    SendMessageRequest,
    PatchConversationRequest,
    CreateConversationSerializer,
    SendMessageSerializer,
    PatchConversationSerializer,
)
from shared.responseutils.response_handler import ResponseHandler
from shared.metadata_handler.request_header_utillity import metadata_handler
from shared.pagination.api_paging import ApiPaging


class ConversationListView(APIView):
    @metadata_handler(required_user_id=True)
    def get(self, request: Request, metadata=None):
        paging = ApiPaging.from_request(request)
        service = conversation_service_factory()
        result = service.list(metadata.user_id, page=paging['page'], page_size=paging['page_size'])
        return ResponseHandler.api_list(result['items'], paging['page'], paging['page_size'], result['total'])

    @metadata_handler(required_user_id=True)
    def post(self, request: Request, metadata=None):
        serializer = CreateConversationRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = conversation_service_factory()
        return ResponseHandler.api_created(service.create(metadata.user_id, {
            'store_id': str(serializer.validated_data['store_id']) if serializer.validated_data.get('store_id') else None,
            'order_id': str(serializer.validated_data['order_id']) if serializer.validated_data.get('order_id') else None,
        }))


class ConversationDetailView(APIView):
    @metadata_handler(required_user_id=True)
    def get(self, request: Request, conversation_id=None, metadata=None):
        service = conversation_service_factory()
        return ResponseHandler.api_success(service.get(str(conversation_id), metadata.user_id))

    @metadata_handler(required_user_id=True)
    def patch(self, request: Request, conversation_id=None, metadata=None):
        serializer = PatchConversationRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = conversation_service_factory()
        if serializer.validated_data.get('status') in ('closed', 'archived'):
            return ResponseHandler.api_success(service.close(str(conversation_id), metadata.user_id))
        return ResponseHandler.api_success(service.get(str(conversation_id), metadata.user_id))


class ConversationMessageListView(APIView):
    @metadata_handler(required_user_id=True)
    def get(self, request: Request, conversation_id=None, metadata=None):
        paging = ApiPaging.from_request(request)
        service = conversation_service_factory()
        result = service.list_messages(str(conversation_id), metadata.user_id, page=paging['page'], page_size=paging['page_size'])
        return ResponseHandler.api_list(result['items'], paging['page'], paging['page_size'], result['total'])

    @metadata_handler(required_user_id=True)
    def post(self, request: Request, conversation_id=None, metadata=None):
        serializer = SendMessageRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = conversation_service_factory()
        return ResponseHandler.api_created(service.send_message(str(conversation_id), metadata.user_id, serializer.validated_data))


class MessageReadView(APIView):
    @metadata_handler(required_user_id=True)
    def post(self, request: Request, message_id=None, metadata=None):
        service = conversation_service_factory()
        return ResponseHandler.api_success(service.mark_read(str(message_id), metadata.user_id))

