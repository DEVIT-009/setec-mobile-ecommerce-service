from rest_framework import viewsets
from rest_framework.request import Request

from application.store.factory.store_service_factory import store_service_factory
from domain.store.exception.store_exception import StoreException
from domain.store.service.store_service import StoreServiceInterface
from interface.store.serializer.request.store_request import StoreRequest, StorePartialRequest
from shared.metadata_handler.request_header_utillity import metadata_handler, Metadata
from shared.permission_handler import require_roles
from shared.pagination.api_paging import ApiPaging
from shared.responseutils.response_handler import ResponseHandler


class StoreAdminView(viewsets.ViewSet):

    store_service: StoreServiceInterface = store_service_factory()

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def list(self, request: Request, *, metadata: Metadata):
        paging = ApiPaging.from_request(request)
        result = self.store_service.list_admin(page=paging['page'], page_size=paging['page_size'])
        return ResponseHandler.api_list(result['items'], paging['page'], paging['page_size'], result['total'])

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def create(self, request: Request, *, metadata: Metadata):
        serializer = StoreRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = self.store_service.create(
            serializer.validated_data,
            actor_id=metadata.user_id,
        )
        return ResponseHandler.api_created(result)

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def retrieve(self, request: Request, store_id=None, *, metadata: Metadata):
        if store_id is None:
            raise StoreException.not_found()
        result = self.store_service.get_by_id(str(store_id))
        return ResponseHandler.api_success(result)

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def retrieve_by_slug(self, request: Request, *, metadata: Metadata):
        slug = request.query_params.get('slug')
        if not slug:
            raise StoreException.not_found("Slug query parameter is required")
        result = self.store_service.get_admin(slug)
        return ResponseHandler.api_success(result)

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def update(self, request: Request, store_id=None, *, metadata: Metadata):
        if store_id is None:
            raise StoreException.not_found()
        serializer = StoreRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = self.store_service.update(
            str(store_id),
            serializer.validated_data,
            actor_id=metadata.user_id,
        )
        return ResponseHandler.api_success(result)

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def partial_update(self, request: Request, store_id=None, *, metadata: Metadata):
        if store_id is None:
            raise StoreException.not_found()
        serializer = StorePartialRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = self.store_service.update(
            str(store_id),
            serializer.validated_data,
            partial=True,
            actor_id=metadata.user_id,
        )
        return ResponseHandler.api_success(result)

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def destroy(self, request: Request, store_id=None, *, metadata: Metadata):
        if store_id is None:
            raise StoreException.not_found()
        self.store_service.soft_delete(str(store_id), actor_id=metadata.user_id)
        return ResponseHandler.api_no_content()
