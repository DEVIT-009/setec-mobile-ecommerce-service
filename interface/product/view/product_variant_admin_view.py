from rest_framework import viewsets
from rest_framework.request import Request

from application.product.factory.product_variant_service_factory import product_variant_service_factory
from domain.product.exception.product_exception import ProductException
from domain.product.service.product_variant_service import ProductVariantServiceInterface
from interface.product.serializer.request.product_variant_request import (
    ProductVariantRequest,
    ProductVariantPartialRequest,
)
from shared.metadata_handler.request_header_utillity import metadata_handler, Metadata
from shared.permission_handler import require_roles
from shared.responseutils.response_handler import ResponseHandler


class ProductVariantAdminView(viewsets.ViewSet):

    variant_service: ProductVariantServiceInterface = product_variant_service_factory()

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def list(self, request: Request, *, metadata: Metadata):
        """GET /api/v1/admin/product/variants/?product_id={product_id}"""
        product_id = request.query_params.get('product_id')
        if not product_id:
            return ResponseHandler.api_success([])
        result = self.variant_service.list_by_product(str(product_id))
        return ResponseHandler.api_success(result)

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def create(self, request: Request, *, metadata: Metadata):
        """POST /api/v1/admin/product/variants/"""
        serializer = ProductVariantRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = self.variant_service.create(serializer.validated_data, actor_id=metadata.user_id)
        return ResponseHandler.api_created(result)

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def retrieve(self, request: Request, variant_id=None, *, metadata: Metadata):
        """GET /api/v1/admin/product/variants/{variant_id}/"""
        if variant_id is None:
            raise ProductException.not_found("Product variant not found")
        result = self.variant_service.get_by_id(str(variant_id))
        return ResponseHandler.api_success(result)

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def update(self, request: Request, variant_id=None, *, metadata: Metadata):
        """PUT /api/v1/admin/product/variants/{variant_id}/"""
        if variant_id is None:
            raise ProductException.not_found("Product variant not found")
        serializer = ProductVariantRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = self.variant_service.update(
            str(variant_id), serializer.validated_data, actor_id=metadata.user_id
        )
        return ResponseHandler.api_success(result)

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def partial_update(self, request: Request, variant_id=None, *, metadata: Metadata):
        """PATCH /api/v1/admin/product/variants/{variant_id}/"""
        if variant_id is None:
            raise ProductException.not_found("Product variant not found")
        serializer = ProductVariantPartialRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = self.variant_service.update(
            str(variant_id), serializer.validated_data, partial=True, actor_id=metadata.user_id
        )
        return ResponseHandler.api_success(result)

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def destroy(self, request: Request, variant_id=None, *, metadata: Metadata):
        """DELETE /api/v1/admin/product/variants/{variant_id}/"""
        if variant_id is None:
            raise ProductException.not_found("Product variant not found")
        self.variant_service.soft_delete(str(variant_id), actor_id=metadata.user_id)
        return ResponseHandler.api_no_content()
