from rest_framework import viewsets
from rest_framework.request import Request

from application.tag.factory.tag_service_factory import tag_service_factory
from domain.tag.exception.tag_exception import TagException
from domain.tag.service.tag_service import TagServiceInterface
from interface.tag.serializer.request.tag_request import TagRequest, TagPartialRequest
from shared.metadata_handler.request_header_utillity import metadata_handler, Metadata
from shared.pagination.api_paging import ApiPaging
from shared.permission_handler import require_roles
from shared.responseutils.response_handler import ResponseHandler


class TagAdminView(viewsets.ViewSet):

    tag_service: TagServiceInterface = tag_service_factory()

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def list(self, request: Request, *, metadata: Metadata):
        paging = ApiPaging.from_request(request)
        result = self.tag_service.list(page=paging['page'], page_size=paging['page_size'])
        return ResponseHandler.api_list(result['items'], paging['page'], paging['page_size'], result['total'])

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def create(self, request: Request, *, metadata: Metadata):
        serializer = TagRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = self.tag_service.create(serializer.validated_data, actor_id=metadata.user_id)
        return ResponseHandler.api_created(result)

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def retrieve(self, request: Request, tag_id=None, *, metadata: Metadata):
        if tag_id is None:
            raise TagException.not_found()
        result = self.tag_service.get(str(tag_id))
        return ResponseHandler.api_success(result)

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def update(self, request: Request, tag_id=None, *, metadata: Metadata):
        if tag_id is None:
            raise TagException.not_found()
        serializer = TagRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = self.tag_service.update(str(tag_id), serializer.validated_data, actor_id=metadata.user_id)
        return ResponseHandler.api_success(result)

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def partial_update(self, request: Request, tag_id=None, *, metadata: Metadata):
        if tag_id is None:
            raise TagException.not_found()
        serializer = TagPartialRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = self.tag_service.update(str(tag_id), serializer.validated_data, partial=True, actor_id=metadata.user_id)
        return ResponseHandler.api_success(result)

    @metadata_handler(required_user_id=True)
    @require_roles("admin")
    def destroy(self, request: Request, tag_id=None, *, metadata: Metadata):
        if tag_id is None:
            raise TagException.not_found()
        self.tag_service.delete(str(tag_id), actor_id=metadata.user_id)
        return ResponseHandler.api_no_content()
