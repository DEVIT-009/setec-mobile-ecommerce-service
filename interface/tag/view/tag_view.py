from rest_framework import viewsets
from rest_framework.request import Request

from application.tag.factory.tag_service_factory import tag_service_factory
from domain.tag.service.tag_service import TagServiceInterface
from shared.metadata_handler.request_header_utillity import metadata_handler, Metadata
from shared.pagination.api_paging import ApiPaging
from shared.responseutils.response_handler import ResponseHandler


class TagPublicView(viewsets.ViewSet):
    """
    Public tag ViewSet (guest access).
    """

    tag_service: TagServiceInterface = tag_service_factory()

    @metadata_handler(required_user_id=False)
    def list(self, request: Request, *, metadata: Metadata):
        paging = ApiPaging.from_request(request)
        result = self.tag_service.list(page=paging['page'], page_size=paging['page_size'])
        return ResponseHandler.api_list(result['items'], paging['page'], paging['page_size'], result['total'])
