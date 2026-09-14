from rest_framework import viewsets
from rest_framework.request import Request

from application.product.factory.product_service_factory import product_service_factory
from domain.product.exception.product_exception import ProductException
from domain.product.service.product_service import ProductServiceInterface
from interface.product.serializer.request.product_request import ProductRequest, ProductPartialRequest
from shared.metadata_handler.request_header_utillity import metadata_handler, Metadata
from shared.pagination.api_paging import ApiPaging
from shared.permission_handler import require_roles
from shared.responseutils.response_handler import ResponseHandler


class ProductAdminView(viewsets.ViewSet):

    product_service: ProductServiceInterface = product_service_factory()

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def list(self, request: Request, *, metadata: Metadata):
        paging = ApiPaging.from_request(request)
        filters = {
            'q': request.query_params.get('q'),
            'category_id': request.query_params.get('category_id'),
            'store_id': request.query_params.get('store_id'),
            'tag': request.query_params.get('tag'),
            'status': request.query_params.get('status'),
            'sort': request.query_params.get('sort', 'newest'),
        }
        result = self.product_service.list_admin(
            filters=filters,
            page=paging['page'],
            page_size=paging['page_size'],
        )
        return ResponseHandler.api_list(result['items'], paging['page'], paging['page_size'], result['total'])

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def create(self, request: Request, *, metadata: Metadata):
        serializer = ProductRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = self.product_service.create(serializer.validated_data, actor_id=metadata.user_id)
        return ResponseHandler.api_created(result)

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def retrieve(self, request: Request, product_id=None, *, metadata: Metadata):
        if product_id is None:
            raise ProductException.not_found()
        result = self.product_service.get_by_id(str(product_id))
        return ResponseHandler.api_success(result)

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def update(self, request: Request, product_id=None, *, metadata: Metadata):
        if product_id is None:
            raise ProductException.not_found()
        serializer = ProductRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = self.product_service.update(str(product_id), serializer.validated_data, actor_id=metadata.user_id)
        return ResponseHandler.api_success(result)

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def partial_update(self, request: Request, product_id=None, *, metadata: Metadata):
        if product_id is None:
            raise ProductException.not_found()
        serializer = ProductPartialRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = self.product_service.update(str(product_id), serializer.validated_data, partial=True, actor_id=metadata.user_id)
        return ResponseHandler.api_success(result)

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def destroy(self, request: Request, product_id=None, *, metadata: Metadata):
        if product_id is None:
            raise ProductException.not_found()
        self.product_service.soft_delete(str(product_id), actor_id=metadata.user_id)
        return ResponseHandler.api_no_content()
