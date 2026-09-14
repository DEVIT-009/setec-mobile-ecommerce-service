from rest_framework.views import APIView
from rest_framework.request import Request

from application.search_history.factory.search_history_service_factory import search_history_service_factory
from interface.search_history.serializer.request.search_history_request import (
    SearchHistoryRecordRequest,
    SearchHistoryRecordSerializer,
)
from shared.responseutils.response_handler import ResponseHandler
from shared.metadata_handler.request_header_utillity import metadata_handler
from shared.pagination.api_paging import ApiPaging


class SearchHistoryListView(APIView):
    @metadata_handler(required_user_id=True)
    def get(self, request: Request, metadata=None):
        paging = ApiPaging.from_request(request)
        service = search_history_service_factory()
        result = service.list(metadata.user_id, page=paging['page'], page_size=paging['page_size'])
        return ResponseHandler.api_list(result['items'], paging['page'], paging['page_size'], result['total'])

    @metadata_handler(required_user_id=True)
    def post(self, request: Request, metadata=None):
        serializer = SearchHistoryRecordRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = search_history_service_factory()
        data = service.record(
            user_id=metadata.user_id,
            query=serializer.validated_data['query'],
            filters_json=serializer.validated_data.get('filters_json'),
            result_count=serializer.validated_data.get('result_count'),
        )
        return ResponseHandler.api_created(data)


    @metadata_handler(required_user_id=True)
    def delete(self, request: Request, metadata=None):
        """Clear all search history for the current user."""
        service = search_history_service_factory()
        service.clear_all(metadata.user_id)
        return ResponseHandler.api_no_content()


class SearchHistoryDetailView(APIView):
    @metadata_handler(required_user_id=True)
    def delete(self, request: Request, search_id=None, metadata=None):
        service = search_history_service_factory()
        service.delete_one(str(search_id), metadata.user_id)
        return ResponseHandler.api_no_content()
