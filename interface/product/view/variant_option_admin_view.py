from rest_framework import viewsets
from rest_framework.request import Request

from application.product.factory.variant_option_service_factory import variant_option_service_factory
from domain.product.exception.product_exception import ProductException
from domain.product.service.variant_option_service import VariantOptionServiceInterface
from interface.product.serializer.request.variant_option_request import (
    VariantOptionRequest,
    VariantOptionPartialRequest,
)
from shared.metadata_handler.request_header_utillity import metadata_handler, Metadata
from shared.permission_handler import require_roles
from shared.responseutils.response_handler import ResponseHandler


class VariantOptionAdminView(viewsets.ViewSet):

    option_service: VariantOptionServiceInterface = variant_option_service_factory()

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def list(self, request: Request, *, metadata: Metadata):
        """GET /api/v1/admin/product/variant-options/?variant_id={variant_id}"""
        variant_id = request.query_params.get('variant_id')
        if not variant_id:
            return ResponseHandler.api_success([])
        result = self.option_service.list_by_variant(str(variant_id))
        return ResponseHandler.api_success(result)

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def create(self, request: Request, *, metadata: Metadata):
        """POST /api/v1/admin/product/variant-options/"""
        serializer = VariantOptionRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = self.option_service.create(serializer.validated_data)
        return ResponseHandler.api_created(result)

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def retrieve(self, request: Request, option_id=None, *, metadata: Metadata):
        """GET /api/v1/admin/product/variant-options/{option_id}/"""
        if option_id is None:
            raise ProductException.not_found("Variant option not found")
        result = self.option_service.get_by_id(str(option_id))
        return ResponseHandler.api_success(result)

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def update(self, request: Request, option_id=None, *, metadata: Metadata):
        """PUT /api/v1/admin/product/variant-options/{option_id}/"""
        if option_id is None:
            raise ProductException.not_found("Variant option not found")
        serializer = VariantOptionRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = self.option_service.update(str(option_id), serializer.validated_data)
        return ResponseHandler.api_success(result)

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def partial_update(self, request: Request, option_id=None, *, metadata: Metadata):
        """PATCH /api/v1/admin/product/variant-options/{option_id}/"""
        if option_id is None:
            raise ProductException.not_found("Variant option not found")
        serializer = VariantOptionPartialRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = self.option_service.update(str(option_id), serializer.validated_data, partial=True)
        return ResponseHandler.api_success(result)

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def destroy(self, request: Request, option_id=None, *, metadata: Metadata):
        """DELETE /api/v1/admin/product/variant-options/{option_id}/"""
        if option_id is None:
            raise ProductException.not_found("Variant option not found")
        self.option_service.delete(str(option_id))
        return ResponseHandler.api_no_content()
