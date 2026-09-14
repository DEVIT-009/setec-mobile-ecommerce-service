from rest_framework import viewsets
from rest_framework.request import Request

from application.product.factory.variant_option_service_factory import variant_option_service_factory
from domain.product.exception.product_exception import ProductException
from domain.product.service.variant_option_service import VariantOptionServiceInterface
from shared.metadata_handler.request_header_utillity import metadata_handler, Metadata
from shared.responseutils.response_handler import ResponseHandler


class VariantOptionPublicView(viewsets.ViewSet):
    """Public variant-option ViewSet — read-only, no authentication required."""

    option_service: VariantOptionServiceInterface = variant_option_service_factory()

    @metadata_handler(required_user_id=False)
    def list(self, request: Request, *, metadata: Metadata):
        """GET /api/v1/public/product/variant-options/?variant_id={variant_id}"""
        variant_id = request.query_params.get('variant_id')
        if not variant_id:
            return ResponseHandler.api_success([])
        result = self.option_service.list_by_variant(str(variant_id))
        return ResponseHandler.api_success(result)

    @metadata_handler(required_user_id=False)
    def retrieve(self, request: Request, option_id=None, *, metadata: Metadata):
        """GET /api/v1/public/product/variant-options/{option_id}/"""
        if option_id is None:
            raise ProductException.not_found("Variant option not found")
        result = self.option_service.get_by_id(str(option_id))
        return ResponseHandler.api_success(result)
