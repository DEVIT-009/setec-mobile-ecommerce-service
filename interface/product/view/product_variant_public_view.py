from rest_framework import viewsets
from rest_framework.request import Request

from application.product.factory.product_variant_service_factory import product_variant_service_factory
from domain.product.exception.product_exception import ProductException
from domain.product.service.product_variant_service import ProductVariantServiceInterface
from shared.metadata_handler.request_header_utillity import metadata_handler, Metadata
from shared.responseutils.response_handler import ResponseHandler


class ProductVariantPublicView(viewsets.ViewSet):
    """Public product-variant ViewSet — read-only, no authentication required."""

    variant_service: ProductVariantServiceInterface = product_variant_service_factory()

    @metadata_handler(required_user_id=False)
    def list(self, request: Request, *, metadata: Metadata):
        """GET /api/v1/public/product/variants/?product_id={product_id}"""
        product_id = request.query_params.get('product_id')
        if not product_id:
            return ResponseHandler.api_success([])
        result = self.variant_service.list_by_product(str(product_id))
        return ResponseHandler.api_success(result)

    @metadata_handler(required_user_id=False)
    def retrieve(self, request: Request, variant_id=None, *, metadata: Metadata):
        """GET /api/v1/public/product/variants/{variant_id}/"""
        if variant_id is None:
            raise ProductException.not_found("Product variant not found")
        result = self.variant_service.get_by_id(str(variant_id))
        return ResponseHandler.api_success(result)
