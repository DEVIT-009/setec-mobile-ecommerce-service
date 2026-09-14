from rest_framework.views import APIView
from rest_framework.request import Request

from application.user.factory.user_service_factory import user_service_factory
from interface.user.serializer.request.user_request import (
    UserUpdateRequest,
    ProfileUpdateRequest,
    SecurityUpdateRequest,
    UserUpdateSerializer,
    ProfileUpdateSerializer,
    SecurityUpdateSerializer,
)
from shared.responseutils.response_handler import ResponseHandler
from shared.metadata_handler.request_header_utillity import metadata_handler


class UserMeView(APIView):
    @metadata_handler(required_user_id=True)
    def get(self, request: Request, metadata=None):
        service = user_service_factory()
        return ResponseHandler.api_success(service.get_me(metadata.user_id))

    @metadata_handler(required_user_id=True)
    def patch(self, request: Request, metadata=None):
        serializer = UserUpdateRequest(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        service = user_service_factory()
        return ResponseHandler.api_success(service.update_me(metadata.user_id, serializer.validated_data))


class UserProfileView(APIView):
    @metadata_handler(required_user_id=True)
    def get(self, request: Request, metadata=None):
        service = user_service_factory()
        return ResponseHandler.api_success(service.get_profile(metadata.user_id))

    @metadata_handler(required_user_id=True)
    def patch(self, request: Request, metadata=None):
        serializer = ProfileUpdateRequest(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        service = user_service_factory()
        return ResponseHandler.api_success(service.update_profile(metadata.user_id, serializer.validated_data))


class UserSecurityView(APIView):
    @metadata_handler(required_user_id=True)
    def get(self, request: Request, metadata=None):
        service = user_service_factory()
        return ResponseHandler.api_success(service.get_security_settings(metadata.user_id))

    @metadata_handler(required_user_id=True)
    def patch(self, request: Request, metadata=None):
        serializer = SecurityUpdateRequest(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        service = user_service_factory()
        return ResponseHandler.api_success(service.update_security_settings(metadata.user_id, serializer.validated_data))



class UserSessionsView(APIView):
    @metadata_handler(required_user_id=True)
    def get(self, request: Request, metadata=None):
        service = user_service_factory()
        return ResponseHandler.api_success(service.list_sessions(metadata.user_id))


class UserSessionRevokeView(APIView):
    @metadata_handler(required_user_id=True)
    def post(self, request: Request, session_id=None, metadata=None):
        service = user_service_factory()
        service.revoke_session(metadata.user_id, session_id)
        return ResponseHandler.api_no_content()

    @metadata_handler(required_user_id=True)
    def delete(self, request: Request, session_id=None, metadata=None):
        service = user_service_factory()
        service.revoke_session(metadata.user_id, session_id)
        return ResponseHandler.api_no_content()

