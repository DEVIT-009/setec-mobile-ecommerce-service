from rest_framework import viewsets
from rest_framework.request import Request

from application.category.factory.category_service_factory import category_service_factory
from domain.category.exception.category_exception import CategoryException
from domain.category.service.category_service import CategoryServiceInterface
from shared.metadata_handler.request_header_utillity import metadata_handler, Metadata
from shared.responseutils.response_handler import ResponseHandler


class CategoryPublicView(viewsets.ViewSet):
    """
    Public category ViewSet (guest access).
    """

    category_service: CategoryServiceInterface = category_service_factory()

    @metadata_handler(required_user_id=False)
    def list(self, request: Request, *, metadata: Metadata):
        parent_id = request.query_params.get('parent_id')
        result = self.category_service.list_active(parent_id=parent_id)
        return ResponseHandler.api_success(result)

    @metadata_handler(required_user_id=False)
    def tree(self, request: Request, *, metadata: Metadata):
        result = self.category_service.get_tree()
        return ResponseHandler.api_success(result)

    @metadata_handler(required_user_id=False)
    def retrieve(self, request: Request, category_id=None, *, metadata: Metadata):
        if category_id is None:
            raise CategoryException.not_found()
        result = self.category_service.get_by_id(str(category_id))
        return ResponseHandler.api_success(result)

    @metadata_handler(required_user_id=False)
    def retrieve_by_slug(self, request: Request, *, metadata: Metadata):
        slug = request.query_params.get('slug')
        if not slug:
            raise CategoryException.not_found("Slug query parameter is required")
        result = self.category_service.get_by_slug(slug)
        return ResponseHandler.api_success(result)
