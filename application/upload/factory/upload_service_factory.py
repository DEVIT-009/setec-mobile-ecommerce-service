from application.upload.upload_service_facade import UploadServiceFacade
from domain.upload.service.upload_service import UploadServiceInterface


def upload_service_factory() -> UploadServiceInterface:
    return UploadServiceFacade()
