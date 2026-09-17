from rest_framework import viewsets
from rest_framework.request import Request

from application.store.factory.store_service_factory import store_service_factory
from domain.store.exception.store_exception import StoreException
from domain.store.service.store_service import StoreServiceInterface
from shared.metadata_handler.request_header_utillity import metadata_handler, Metadata
from shared.pagination.api_paging import ApiPaging
from shared.responseutils.response_handler import ResponseHandler


class StorePublicView(viewsets.ViewSet):
    """
    Public store ViewSet (guest access).
    """

    store_service: StoreServiceInterface = store_service_factory()

    @metadata_handler(required_user_id=False)
    def list(self, request: Request, *, metadata: Metadata):
        paging = ApiPaging.from_request(request)
        result = self.store_service.list_active(page=paging['page'], page_size=paging['page_size'])
        return ResponseHandler.api_list(result['items'], paging['page'], paging['page_size'], result['total'])

    @metadata_handler(required_user_id=False)
    def retrieve(self, request: Request, store_id=None, *, metadata: Metadata):
        if store_id is None:
            raise StoreException.not_found()
        result = self.store_service.get_by_id(str(store_id))
        return ResponseHandler.api_success(result)

    @metadata_handler(required_user_id=False)
    def retrieve_by_slug(self, request: Request, *, metadata: Metadata):
        slug = request.query_params.get('slug')
        if not slug:
            raise StoreException.not_found("Slug query parameter is required")
        result = self.store_service.get_by_slug(slug)
        return ResponseHandler.api_success(result)

    @metadata_handler(required_user_id=False, optional_user_id=True)
    def products(self, request: Request, store_id=None, *, metadata: Metadata):
        if store_id is None:
            raise StoreException.not_found()
        paging = ApiPaging.from_request(request)
        result = self.store_service.list_products(
            str(store_id),
            page=paging['page'],
            page_size=paging['page_size'],
            user_id=metadata.user_id,
        )
        return ResponseHandler.api_success(result)

    @metadata_handler(required_user_id=False, optional_user_id=True)
    def products_by_slug(self, request: Request, *, metadata: Metadata):
        slug = request.query_params.get('slug')
        if not slug:
            raise StoreException.not_found("Slug query parameter is required")
        paging = ApiPaging.from_request(request)
        result = self.store_service.list_products_by_slug(
            slug,
            page=paging['page'],
            page_size=paging['page_size'],
            user_id=metadata.user_id,
        )
        return ResponseHandler.api_success(result)
