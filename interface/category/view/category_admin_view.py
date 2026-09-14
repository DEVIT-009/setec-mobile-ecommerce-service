from rest_framework import viewsets
from rest_framework.request import Request

from application.category.factory.category_service_factory import category_service_factory
from domain.category.exception.category_exception import CategoryException
from domain.category.service.category_service import CategoryServiceInterface
from interface.category.serializer.request.category_request import CategoryRequest, CategoryPartialRequest
from shared.metadata_handler.request_header_utillity import metadata_handler, Metadata
from shared.permission_handler import require_roles
from shared.responseutils.response_handler import ResponseHandler


class CategoryAdminView(viewsets.ViewSet):

    category_service: CategoryServiceInterface = category_service_factory()

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def list(self, request: Request, *, metadata: Metadata):
        parent_id = request.query_params.get('parent_id')
        result = self.category_service.list_admin(parent_id=parent_id)
        return ResponseHandler.api_success(result)

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def create(self, request: Request, *, metadata: Metadata):
        serializer = CategoryRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = self.category_service.create(
            serializer.validated_data,
            actor_id=metadata.user_id,
        )
        return ResponseHandler.api_created(result)

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def retrieve(self, request: Request, category_id=None, *, metadata: Metadata):
        if category_id is None:
            raise CategoryException.not_found()
        result = self.category_service.get_by_id(str(category_id))
        return ResponseHandler.api_success(result)

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def retrieve_by_slug(self, request: Request, *, metadata: Metadata):
        slug = request.query_params.get('slug')
        if not slug:
            raise CategoryException.not_found("Slug query parameter is required")
        result = self.category_service.get_admin(slug)
        return ResponseHandler.api_success(result)

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def update(self, request: Request, category_id=None, *, metadata: Metadata):
        if category_id is None:
            raise CategoryException.not_found()
        serializer = CategoryRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = self.category_service.update(
            str(category_id),
            serializer.validated_data,
            actor_id=metadata.user_id,
        )
        return ResponseHandler.api_success(result)

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def partial_update(self, request: Request, category_id=None, *, metadata: Metadata):
        if category_id is None:
            raise CategoryException.not_found()
        serializer = CategoryPartialRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = self.category_service.update(
            str(category_id),
            serializer.validated_data,
            partial=True,
            actor_id=metadata.user_id,
        )
        return ResponseHandler.api_success(result)

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def destroy(self, request: Request, category_id=None, *, metadata: Metadata):
        if category_id is None:
            raise CategoryException.not_found()
        self.category_service.soft_delete(str(category_id), actor_id=metadata.user_id)
        return ResponseHandler.api_no_content()
