from rest_framework.views import APIView
from rest_framework.request import Request

from application.upload.factory.upload_service_factory import upload_service_factory
from interface.upload.serializer.request.upload_request import (
    CloudinarySignatureRequest,
    ConfirmUploadRequest,
    CloudinarySignatureSerializer,
    ConfirmUploadSerializer,
)
from shared.responseutils.response_handler import ResponseHandler
from shared.metadata_handler.request_header_utillity import metadata_handler


class CloudinarySignatureView(APIView):
    @metadata_handler(required_user_id=True)
    def post(self, request: Request, metadata=None):
        serializer = CloudinarySignatureRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = upload_service_factory()
        data = service.generate_signature(folder=serializer.validated_data.get('folder', 'uploads'))
        return ResponseHandler.api_success(data)


class ConfirmUploadView(APIView):
    @metadata_handler(required_user_id=True)
    def post(self, request: Request, metadata=None):
        serializer = ConfirmUploadRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = upload_service_factory()
        data = service.confirm_upload(metadata.user_id, serializer.validated_data)
        return ResponseHandler.api_success(data)

