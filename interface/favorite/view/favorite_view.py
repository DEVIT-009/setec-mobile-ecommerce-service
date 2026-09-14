from rest_framework.views import APIView
from rest_framework.request import Request

from application.favorite.factory.favorite_service_factory import favorite_service_factory
from interface.favorite.serializer.request.favorite_request import AddFavoriteRequest, AddFavoriteSerializer
from shared.responseutils.response_handler import ResponseHandler
from shared.metadata_handler.request_header_utillity import metadata_handler
from shared.pagination.api_paging import ApiPaging


class FavoriteListView(APIView):
    @metadata_handler(required_user_id=True)
    def get(self, request: Request, metadata=None):
        paging = ApiPaging.from_request(request)
        service = favorite_service_factory()
        result = service.list(metadata.user_id, page=paging['page'], page_size=paging['page_size'])
        return ResponseHandler.api_list(result['items'], paging['page'], paging['page_size'], result['total'])

    @metadata_handler(required_user_id=True)
    def post(self, request: Request, metadata=None):
        serializer = AddFavoriteRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = favorite_service_factory()
        return ResponseHandler.api_created(service.add(metadata.user_id, str(serializer.validated_data['product_id'])))



class FavoriteDeleteView(APIView):
    @metadata_handler(required_user_id=True)
    def delete(self, request: Request, product_id=None, metadata=None):
        service = favorite_service_factory()
        service.remove(metadata.user_id, str(product_id))
        return ResponseHandler.api_no_content()
