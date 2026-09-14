from typing import List, Optional, Tuple
from domain.support_ticket.ports.support_repository import SupportRepositoryInterface
from domain.support_ticket.entity.support_ticket import SupportTicket, SupportMessage
from infrastructure.persistence.mapper.support_persistence_mapper import SupportPersistenceMapper
from infrastructure.persistence.models.support_model import (
    SupportTicket as SupportTicketModel,
    SupportTicketMessage as SupportTicketMessageModel,
)


class SupportRepositoryInterfaceImpl(SupportRepositoryInterface):

    def list_by_user(self, user_id: str, page: int, page_size: int) -> Tuple[List[SupportTicket], int]:
        qs = SupportTicketModel.objects.filter(user_id=user_id, deleted_at__isnull=True).order_by('-created_at')
        total = qs.count()
        offset = (page - 1) * page_size
        models = list(qs[offset:offset + page_size])
        return [SupportPersistenceMapper.from_entity(m) for m in models if m is not None], total

    def create(self, ticket: SupportTicket) -> SupportTicket:
        model = SupportPersistenceMapper.to_model(ticket)
        model.save()
        return SupportPersistenceMapper.from_entity(model)

    def get_by_id(self, ticket_id: str, user_id: Optional[str] = None) -> Optional[SupportTicket]:
        qs = SupportTicketModel.objects.filter(id=ticket_id, deleted_at__isnull=True)
        if user_id:
            qs = qs.filter(user_id=user_id)
        model = qs.first()
        if not model:
            return None
        return SupportPersistenceMapper.from_entity(model)

    def save(self, ticket: SupportTicket) -> SupportTicket:
        db_instance = SupportTicketModel.objects.filter(pk=ticket.id).first() if ticket.id else None
        db_instance = SupportPersistenceMapper.to_model(ticket, db_instance)
        db_instance.save()
        return SupportPersistenceMapper.from_entity(db_instance)

    def list_messages(self, ticket_id: str, page: int, page_size: int) -> Tuple[List[SupportMessage], int]:
        qs = SupportTicketMessageModel.objects.filter(ticket_id=ticket_id, deleted_at__isnull=True).order_by('created_at')
        total = qs.count()
        offset = (page - 1) * page_size
        models = list(qs[offset:offset + page_size])
        return [SupportPersistenceMapper.message_from_entity(m) for m in models if m is not None], total

    def add_message(self, msg: SupportMessage) -> SupportMessage:
        model = SupportPersistenceMapper.message_to_model(msg)
        model.save()
        return SupportPersistenceMapper.message_from_entity(model)
