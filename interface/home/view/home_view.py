from rest_framework.views import APIView
from rest_framework.request import Request

from application.home.factory.home_service_factory import home_service_factory
from shared.responseutils.response_handler import ResponseHandler
from shared.metadata_handler.request_header_utillity import metadata_handler


class HomeView(APIView):
    @metadata_handler(required_user_id=False, optional_user_id=True)
    def get(self, request: Request, metadata=None):
        service = home_service_factory()
        return ResponseHandler.api_success(service.get_home(user_id=metadata.user_id))
