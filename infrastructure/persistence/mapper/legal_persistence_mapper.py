from typing import Optional
from domain.legal_document.entity.legal_document import (
    LegalDocument as DomainLegalDocument,
    LegalAcceptance as DomainLegalAcceptance,
)
from infrastructure.persistence.models.legal_model import (
    LegalDocument as LegalDocumentModel,
    LegalAcceptance as LegalAcceptanceModel,
)


class LegalPersistenceMapper:

    @staticmethod
    def from_entity(entity: Optional[LegalDocumentModel]) -> Optional[DomainLegalDocument]:
        if entity is None:
            return None
        return DomainLegalDocument(
            id=str(entity.id),
            type=entity.type,
            title=entity.title,
            version=entity.version,
            content=entity.content,
            published_at=entity.published_at,
            status=entity.status,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            deleted_at=entity.deleted_at,
        )

    @staticmethod
    def to_model(domain: DomainLegalDocument, model_instance: Optional[LegalDocumentModel] = None) -> LegalDocumentModel:
        model = model_instance or LegalDocumentModel()
        model.type = domain.type
        model.title = domain.title
        model.version = domain.version
        model.content = domain.content
        model.published_at = domain.published_at
        model.status = domain.status
        model.deleted_at = domain.deleted_at
        return model

    @staticmethod
    def acceptance_from_entity(entity: Optional[LegalAcceptanceModel]) -> Optional[DomainLegalAcceptance]:
        if entity is None:
            return None
        return DomainLegalAcceptance(
            id=str(entity.id),
            user_id=str(entity.user_id) if entity.user_id else None,
            legal_document_id=str(entity.legal_document_id) if entity.legal_document_id else None,
            accepted_at=entity.accepted_at,
            ip_address=entity.ip_address,
        )

    @staticmethod
    def acceptance_to_model(domain: DomainLegalAcceptance, model_instance: Optional[LegalAcceptanceModel] = None) -> LegalAcceptanceModel:
        model = model_instance or LegalAcceptanceModel()
        if domain.user_id:
            model.user_id = domain.user_id
        if domain.legal_document_id:
            model.legal_document_id = domain.legal_document_id
        model.ip_address = domain.ip_address
        return model
