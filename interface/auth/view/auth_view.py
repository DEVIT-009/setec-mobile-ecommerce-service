from rest_framework.views import APIView
from rest_framework.request import Request

from application.auth.factory.auth_service_factory import auth_service_factory
from interface.auth.serializer.request.auth_request import (
    RegisterRequest,
    LoginRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    VerifyPhoneRequest,
    RegisterSerializer,
    LoginSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
    VerifyPhoneSerializer,
)
from shared.responseutils.response_handler import ResponseHandler
from shared.metadata_handler.request_header_utillity import metadata_handler
from shared.security.jwt_util import JwtUtil


class RegisterView(APIView):
    def post(self, request: Request):
        serializer = RegisterRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = auth_service_factory()
        data = service.register(**serializer.validated_data)
        return ResponseHandler.api_created(data)


class LoginView(APIView):
    def post(self, request: Request):
        serializer = LoginRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = auth_service_factory()
        data = service.login(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password'],
            request=request,
        )
        return ResponseHandler.api_success(data)


class LogoutView(APIView):
    @metadata_handler(required_user_id=True)

    def post(self, request: Request, metadata=None):
        # Extract session_id from JWT if present
        auth_header = request.headers.get("Authorization", "")
        session_id = None
        if auth_header.startswith("Bearer "):
            token = auth_header[7:]
            try:
                import jwt as pyjwt
                from django.conf import settings
                payload = pyjwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                session_id = payload.get("session_id")
            except Exception:
                pass
        service = auth_service_factory()
        service.logout(metadata.user_id, session_id=session_id)
        return ResponseHandler.api_no_content()


class RefreshView(APIView):
    @metadata_handler(required_user_id=True)
    def post(self, request: Request, metadata=None):
        auth_header = request.headers.get("Authorization", "")
        session_id = None
        if auth_header.startswith("Bearer "):
            token = auth_header[7:]
            try:
                import jwt as pyjwt
                from django.conf import settings
                payload = pyjwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                session_id = payload.get("session_id")
            except Exception:
                pass
        service = auth_service_factory()
        data = service.refresh(metadata.user_id, session_id=session_id)
        return ResponseHandler.api_success(data)


class ForgotPasswordView(APIView):
    def post(self, request: Request):
        serializer = ForgotPasswordRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = auth_service_factory()
        data = service.forgot_password(serializer.validated_data['email'])
        return ResponseHandler.api_success(data)


class ResetPasswordView(APIView):
    def post(self, request: Request):
        serializer = ResetPasswordRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = auth_service_factory()
        data = service.reset_password(
            serializer.validated_data['reset_token'],
            serializer.validated_data['new_password'],
        )
        return ResponseHandler.api_success(data)


class VerifyEmailView(APIView):
    @metadata_handler(required_user_id=True)
    def post(self, request: Request, metadata=None):
        service = auth_service_factory()
        data = service.verify_email(metadata.user_id)
        return ResponseHandler.api_success(data)


class VerifyPhoneView(APIView):
    @metadata_handler(required_user_id=True)
    def post(self, request: Request, metadata=None):
        serializer = VerifyPhoneRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = auth_service_factory()
        data = service.verify_phone(metadata.user_id, serializer.validated_data.get('phone_number'))
        return ResponseHandler.api_success(data)



class AuthMeView(APIView):
    @metadata_handler(required_user_id=True)
    def get(self, request: Request, metadata=None):
        service = auth_service_factory()
        data = service.get_me(metadata.user_id)
        return ResponseHandler.api_success(data)
