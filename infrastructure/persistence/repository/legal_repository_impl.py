from typing import List, Optional, Tuple
from domain.legal_document.ports.legal_repository import LegalRepositoryInterface
from domain.legal_document.entity.legal_document import LegalDocument, LegalAcceptance
from infrastructure.persistence.mapper.legal_persistence_mapper import LegalPersistenceMapper
from infrastructure.persistence.models.legal_model import (
    LegalDocument as LegalDocumentModel,
    LegalAcceptance as LegalAcceptanceModel,
)


class LegalRepositoryInterfaceImpl(LegalRepositoryInterface):

    def list_published(self, doc_type: Optional[str] = None) -> List[LegalDocument]:
        qs = LegalDocumentModel.objects.filter(status='published', deleted_at__isnull=True).order_by('type', '-created_at')
        if doc_type:
            qs = qs.filter(type=doc_type)
        return [LegalPersistenceMapper.from_entity(m) for m in qs if m is not None]

    def get_latest_by_type(self, doc_type: str) -> Optional[LegalDocument]:
        model = LegalDocumentModel.objects.filter(type=doc_type, status='published', deleted_at__isnull=True).order_by('-published_at').first()
        if not model:
            return None
        return LegalPersistenceMapper.from_entity(model)

    def get_by_id(self, doc_id: str) -> Optional[LegalDocument]:
        model = LegalDocumentModel.objects.filter(id=doc_id, deleted_at__isnull=True).first()
        if not model:
            return None
        return LegalPersistenceMapper.from_entity(model)

    def record_acceptance(self, acceptance: LegalAcceptance) -> LegalAcceptance:
        model, _ = LegalAcceptanceModel.objects.get_or_create(
            user_id=acceptance.user_id,
            legal_document_id=acceptance.legal_document_id,
            defaults={'ip_address': acceptance.ip_address},
        )
        return LegalPersistenceMapper.acceptance_from_entity(model)

    def list_acceptances(self, user_id: str) -> List[LegalAcceptance]:
        models = LegalAcceptanceModel.objects.filter(user_id=user_id).select_related('legal_document').order_by('-accepted_at')
        return [LegalPersistenceMapper.acceptance_from_entity(m) for m in models if m is not None]
