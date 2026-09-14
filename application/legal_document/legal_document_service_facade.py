from typing import Dict, Any, List, Optional
from django.utils import timezone
from domain.legal_document.ports.legal_repository import LegalRepositoryInterface
from domain.legal_document.service.legal_service import LegalServiceInterface
from domain.legal_document.entity.legal_document import LegalDocument, LegalAcceptance
from domain.legal_document.exception.legal_exception import LegalException
from interface.legal_document.serializer.mapper.legal_controller_mapper import LegalControllerMapper


class LegalDocumentServiceFacade(LegalServiceInterface):

    def __init__(self, repo: LegalRepositoryInterface):
        self.repo = repo

    def list_published(self, doc_type: Optional[str] = None) -> List[Dict[str, Any]]:
        docs = self.repo.list_published(doc_type)
        return LegalControllerMapper.to_list_response(docs)

    def get_latest_by_type(self, doc_type: str) -> Dict[str, Any]:
        doc = self.repo.get_latest_by_type(doc_type)
        if not doc:
            raise LegalException.not_found()
        return LegalControllerMapper.to_response(doc)

    def get_latest(self, doc_type: str) -> Dict[str, Any]:
        return self.get_latest_by_type(doc_type)

    def accept(self, user_id: str, doc_id: str, ip_address: Optional[str] = None) -> Dict[str, Any]:
        doc = self.repo.get_by_id(doc_id)
        if not doc:
            raise LegalException.not_found()
        acc = LegalAcceptance(user_id=user_id, legal_document_id=doc_id, ip_address=ip_address)
        saved = self.repo.record_acceptance(acc)
        return LegalControllerMapper.acceptance_to_response(saved)

    def list_user_acceptances(self, user_id: str) -> List[Dict[str, Any]]:
        accs = self.repo.list_acceptances(user_id)
        return LegalControllerMapper.acceptance_to_list_response(accs)

    def list_acceptances(self, user_id: str) -> List[Dict[str, Any]]:
        return self.list_user_acceptances(user_id)

    def list_admin_versions(self, doc_type: Optional[str] = None) -> List[Dict[str, Any]]:
        from infrastructure.persistence.models.legal_model import LegalDocument as LegalDocumentModel
        qs = LegalDocumentModel.objects.filter(deleted_at__isnull=True).order_by('type', '-created_at')
        if doc_type:
            qs = qs.filter(type=doc_type)
        from infrastructure.persistence.mapper.legal_persistence_mapper import LegalPersistenceMapper
        docs = [LegalPersistenceMapper.from_entity(m) for m in qs if m is not None]
        return LegalControllerMapper.to_list_response(docs)

    def create_admin_version(self, data: dict) -> Dict[str, Any]:
        from infrastructure.persistence.models.legal_model import LegalDocument as LegalDocumentModel
        doc = LegalDocumentModel.objects.create(
            type=data['type'],
            title=data['title'],
            version=data['version'],
            content=data['content'],
            status='draft',
        )
        from infrastructure.persistence.mapper.legal_persistence_mapper import LegalPersistenceMapper
        return LegalControllerMapper.to_response(LegalPersistenceMapper.from_entity(doc))

    def update_admin_version(self, doc_id: str, data: dict) -> Dict[str, Any]:
        doc = self.repo.get_by_id(doc_id)
        if not doc:
            raise LegalException.not_found()
        for field in ['title', 'content', 'version']:
            if field in data:
                setattr(doc, field, data[field])
        from infrastructure.persistence.models.legal_model import LegalDocument as LegalDocumentModel
        from infrastructure.persistence.mapper.legal_persistence_mapper import LegalPersistenceMapper
        db_instance = LegalDocumentModel.objects.filter(id=doc_id).first()
        db_instance = LegalPersistenceMapper.to_model(doc, db_instance)
        db_instance.save()
        return LegalControllerMapper.to_response(LegalPersistenceMapper.from_entity(db_instance))

    def publish_admin_version(self, doc_id: str) -> Dict[str, Any]:
        doc = self.repo.get_by_id(doc_id)
        if not doc:
            raise LegalException.not_found()
        doc.status = 'published'
        doc.published_at = timezone.now()
        from infrastructure.persistence.models.legal_model import LegalDocument as LegalDocumentModel
        from infrastructure.persistence.mapper.legal_persistence_mapper import LegalPersistenceMapper
        db_instance = LegalDocumentModel.objects.filter(id=doc_id).first()
        db_instance = LegalPersistenceMapper.to_model(doc, db_instance)
        db_instance.save()
        return LegalControllerMapper.to_response(LegalPersistenceMapper.from_entity(db_instance))

    def archive_admin_version(self, doc_id: str) -> Dict[str, Any]:
        doc = self.repo.get_by_id(doc_id)
        if not doc:
            raise LegalException.not_found()
        doc.status = 'archived'
        from infrastructure.persistence.models.legal_model import LegalDocument as LegalDocumentModel
        from infrastructure.persistence.mapper.legal_persistence_mapper import LegalPersistenceMapper
        db_instance = LegalDocumentModel.objects.filter(id=doc_id).first()
        db_instance = LegalPersistenceMapper.to_model(doc, db_instance)
        db_instance.save()
        return LegalControllerMapper.to_response(LegalPersistenceMapper.from_entity(db_instance))
