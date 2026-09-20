from rest_framework import viewsets
from rest_framework.request import Request

from application.search_history.factory.search_history_service_factory import search_history_service_factory
from domain.search_history.service.search_service import SearchServiceInterface
from interface.search_history.serializer.request.search_history_request import SearchHistoryRecordRequest
from shared.metadata_handler.request_header_utillity import metadata_handler, Metadata
from shared.pagination.api_paging import ApiPaging
from shared.responseutils.response_handler import ResponseHandler


class SearchHistoryCustomerView(viewsets.ViewSet):
    search_history_service: SearchServiceInterface = search_history_service_factory()

    @metadata_handler(required_user_id=True)
    def list(self, request: Request, *, metadata: Metadata):
        paging = ApiPaging.from_request(request)
        result = self.search_history_service.list(
            metadata.user_id,
            page=paging['page'],
            page_size=paging['page_size'],
        )
        return ResponseHandler.api_list(result['items'], paging['page'], paging['page_size'], result['total'])

    @metadata_handler(required_user_id=True)
    def create(self, request: Request, *, metadata: Metadata):
        serializer = SearchHistoryRecordRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = self.search_history_service.record(
            user_id=metadata.user_id,
            data=serializer.validated_data,
        )
        return ResponseHandler.api_created(result)

    @metadata_handler(required_user_id=True)
    def destroy(self, request: Request, search_id=None, *, metadata: Metadata):
        self.search_history_service.delete_one(str(search_id), metadata.user_id)
        return ResponseHandler.api_no_content()

    @metadata_handler(required_user_id=True)
    def clear(self, request: Request, *, metadata: Metadata):
        self.search_history_service.clear_all(metadata.user_id)
        return ResponseHandler.api_no_content()
