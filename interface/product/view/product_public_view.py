from rest_framework import viewsets
from rest_framework.request import Request

from application.product.factory.product_service_factory import product_service_factory
from domain.product.exception.product_exception import ProductException
from domain.product.service.product_service import ProductServiceInterface
from shared.metadata_handler.request_header_utillity import metadata_handler, Metadata
from shared.pagination.api_paging import ApiPaging
from shared.responseutils.response_handler import ResponseHandler


class ProductPublicView(viewsets.ViewSet):
    """Public product ViewSet — read-only, no authentication required."""

    product_service: ProductServiceInterface = product_service_factory()

    @metadata_handler(required_user_id=False, optional_user_id=True)
    def list(self, request: Request, *, metadata: Metadata):
        paging = ApiPaging.from_request(request)
        filters = {
            'q': request.query_params.get('q'),
            'category_id': request.query_params.get('category_id'),
            'store_id': request.query_params.get('store_id'),
            'tag': request.query_params.get('tag'),
            'min_price': request.query_params.get('min_price'),
            'max_price': request.query_params.get('max_price'),
            'rating_min': request.query_params.get('rating_min'),
            'status': request.query_params.get('status'),
            'sort': request.query_params.get('sort', 'newest'),
        }
        result = self.product_service.list_active(
            filters=filters,
            page=paging['page'],
            page_size=paging['page_size'],
            user_id=metadata.user_id,
        )
        return ResponseHandler.api_list(result['items'], paging['page'], paging['page_size'], result['total'])

    @metadata_handler(required_user_id=False, optional_user_id=True)
    def retrieve(self, request: Request, product_id=None, *, metadata: Metadata):
        if product_id is None:
            raise ProductException.not_found()
        result = self.product_service.get_by_id(str(product_id), user_id=metadata.user_id)
        return ResponseHandler.api_success(result)

    @metadata_handler(required_user_id=False, optional_user_id=True)
    def retrieve_by_store_slug(self, request: Request, store_slug=None, product_slug=None, *, metadata: Metadata):
        """GET /public/products/slug/<store_slug>/<product_slug>/"""
        result = self.product_service.get_by_store_and_slug(store_slug, product_slug, user_id=metadata.user_id)
        return ResponseHandler.api_success(result)

    @metadata_handler(required_user_id=False)
    def images(self, request: Request, product_id=None, *, metadata: Metadata):
        if product_id is None:
            raise ProductException.not_found()
        result = self.product_service.get_images(str(product_id))
        return ResponseHandler.api_success(result)

    @metadata_handler(required_user_id=False)
    def variants(self, request: Request, product_id=None, *, metadata: Metadata):
        if product_id is None:
            raise ProductException.not_found()
        result = self.product_service.get_variants(str(product_id))
        return ResponseHandler.api_success(result)

    @metadata_handler(required_user_id=False)
    def reviews(self, request: Request, product_id=None, *, metadata: Metadata):
        if product_id is None:
            raise ProductException.not_found()
        paging = ApiPaging.from_request(request)
        result = self.product_service.get_reviews(str(product_id), page=paging['page'], page_size=paging['page_size'])
        return ResponseHandler.api_list(result['items'], paging['page'], paging['page_size'], result['total'])

    @metadata_handler(required_user_id=True)
    def favorite_state(self, request: Request, product_id=None, *, metadata: Metadata):
        if product_id is None:
            raise ProductException.not_found()
        result = self.product_service.get_favorite_state(str(product_id), metadata.user_id)
        return ResponseHandler.api_success(result)

    @metadata_handler(required_user_id=False)
    def list_tags(self, request: Request, *, metadata: Metadata):
        paging = ApiPaging.from_request(request)
        result = self.product_service.list_tags(page=paging['page'], page_size=paging['page_size'])
        return ResponseHandler.api_list(result['items'], paging['page'], paging['page_size'], result['total'])
