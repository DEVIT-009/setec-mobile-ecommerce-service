from rest_framework import viewsets
from rest_framework.request import Request

from application.address.factory.address_service_factory import address_service_factory
from domain.address.exception.address_exception import AddressException
from domain.address.service.address_service import AddressServiceInterface
from interface.address.serializer.request.address_request import AddressRequest, AddressPartialRequest
from shared.metadata_handler.request_header_utillity import metadata_handler, Metadata
from shared.responseutils.response_handler import ResponseHandler


class AddressCustomerView(viewsets.ViewSet):

    address_service: AddressServiceInterface = address_service_factory()

    @metadata_handler(required_user_id=True)
    def list(self, request: Request, *, metadata: Metadata):
        result = self.address_service.list(metadata.user_id)
        return ResponseHandler.api_success(result)

    @metadata_handler(required_user_id=True)
    def create(self, request: Request, *, metadata: Metadata):
        serializer = AddressRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = self.address_service.create(
            metadata.user_id,
            serializer.validated_data,
            actor_id=metadata.user_id,
        )
        return ResponseHandler.api_created(result)

    @metadata_handler(required_user_id=True)
    def retrieve(self, request: Request, address_id=None, *, metadata: Metadata):
        if address_id is None:
            raise AddressException.not_found()
        result = self.address_service.get(str(address_id), metadata.user_id)
        return ResponseHandler.api_success(result)

    @metadata_handler(required_user_id=True)
    def update(self, request: Request, address_id=None, *, metadata: Metadata):
        if address_id is None:
            raise AddressException.not_found()
        serializer = AddressRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = self.address_service.update(
            str(address_id),
            metadata.user_id,
            serializer.validated_data,
            partial=False,
            actor_id=metadata.user_id,
        )
        return ResponseHandler.api_success(result)

    @metadata_handler(required_user_id=True)
    def partial_update(self, request: Request, address_id=None, *, metadata: Metadata):
        if address_id is None:
            raise AddressException.not_found()
        serializer = AddressPartialRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = self.address_service.update(
            str(address_id),
            metadata.user_id,
            serializer.validated_data,
            partial=True,
            actor_id=metadata.user_id,
        )
        return ResponseHandler.api_success(result)

    @metadata_handler(required_user_id=True)
    def destroy(self, request: Request, address_id=None, *, metadata: Metadata):
        if address_id is None:
            raise AddressException.not_found()
        self.address_service.delete(
            str(address_id),
            metadata.user_id,
            actor_id=metadata.user_id,
        )
        return ResponseHandler.api_no_content()

    @metadata_handler(required_user_id=True)
    def set_default(self, request: Request, address_id=None, *, metadata: Metadata):
        if address_id is None:
            raise AddressException.not_found()
        result = self.address_service.set_default(
            str(address_id),
            metadata.user_id,
            actor_id=metadata.user_id,
        )
        return ResponseHandler.api_success(result)
