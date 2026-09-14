from application.legal_document.legal_document_service_facade import LegalDocumentServiceFacade
from domain.legal_document.service.legal_service import LegalServiceInterface
from infrastructure.persistence.repository.legal_repository_impl import LegalRepositoryInterfaceImpl


def legal_document_service_factory() -> LegalServiceInterface:
    repo = LegalRepositoryInterfaceImpl()
    return LegalDocumentServiceFacade(repo)
