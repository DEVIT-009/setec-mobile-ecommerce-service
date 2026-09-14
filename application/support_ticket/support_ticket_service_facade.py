from typing import Dict, Any
from domain.support_ticket.ports.support_repository import SupportRepositoryInterface
from domain.support_ticket.service.support_service import SupportServiceInterface
from domain.support_ticket.entity.support_ticket import SupportTicket, SupportMessage
from domain.support_ticket.exception.support_exception import SupportException
from interface.support_ticket.serializer.mapper.support_controller_mapper import SupportControllerMapper


class SupportTicketServiceFacade(SupportServiceInterface):

    def __init__(self, repo: SupportRepositoryInterface):
        self.repo = repo

    def list_tickets(self, user_id: str, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        tickets, total = self.repo.list_by_user(user_id, page, page_size)
        return {
            "items": SupportControllerMapper.to_list_response(tickets),
            "total": total,
        }

    def create_ticket(self, user_id: str, data: dict) -> Dict[str, Any]:
        ticket = SupportTicket(
            user_id=user_id,
            order_id=data.get('order_id'),
            subject=data['subject'],
            category=data.get('category', 'other'),
            priority=data.get('priority', 'normal'),
            status='open',
        )
        saved = self.repo.create(ticket)
        if data.get('initial_message'):
            msg = SupportMessage(
                ticket_id=saved.id,
                sender_id=user_id,
                body=data['initial_message'],
            )
            self.repo.add_message(msg)
        return SupportControllerMapper.to_response(saved)

    def get_ticket(self, user_id: str, ticket_id: str) -> Dict[str, Any]:
        ticket = self.repo.get_by_id(ticket_id, user_id)
        if not ticket:
            raise SupportException.not_found()
        return SupportControllerMapper.to_response(ticket)

    def update_ticket(self, user_id: str, ticket_id: str, data: dict) -> Dict[str, Any]:
        ticket = self.repo.get_by_id(ticket_id, user_id)
        if not ticket:
            raise SupportException.not_found()
        if 'subject' in data:
            ticket.subject = data['subject']
        if 'status' in data:
            ticket.status = data['status']
        saved = self.repo.save(ticket)
        return SupportControllerMapper.to_response(saved)

    def list_messages(self, user_id: str, ticket_id: str, page: int = 1, page_size: int = 30) -> Dict[str, Any]:
        ticket = self.repo.get_by_id(ticket_id, user_id)
        if not ticket:
            raise SupportException.not_found()
        msgs, total = self.repo.list_messages(ticket_id, page, page_size)
        return {
            "items": SupportControllerMapper.message_to_list_response(msgs),
            "total": total,
        }

    def add_message(self, user_id: str, ticket_id: str, data: dict) -> Dict[str, Any]:
        ticket = self.repo.get_by_id(ticket_id, user_id)
        if not ticket:
            raise SupportException.not_found()
        msg = SupportMessage(
            ticket_id=ticket_id,
            sender_id=user_id,
            body=data['body'],
            attachment_url=data.get('attachment_url'),
        )
        saved = self.repo.add_message(msg)
        return SupportControllerMapper.message_to_response(saved)

    def list_admin_tickets(self, filters: dict, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        from infrastructure.persistence.models.support_model import SupportTicket as SupportTicketModel
        qs = SupportTicketModel.objects.filter(deleted_at__isnull=True).order_by('-created_at')
        if filters.get('status'):
            qs = qs.filter(status=filters['status'])
        if filters.get('category'):
            qs = qs.filter(category=filters['category'])
        if filters.get('priority'):
            qs = qs.filter(priority=filters['priority'])
        total = qs.count()
        offset = (page - 1) * page_size
        models = list(qs[offset:offset + page_size])
        return {
            "items": [
                {
                    "id": str(t.id), "user_id": str(t.user_id), "order_id": str(t.order_id) if t.order_id else None,
                    "subject": t.subject, "category": t.category, "status": t.status, "priority": t.priority,
                    "created_at": t.created_at.isoformat() if t.created_at else None,
                }
                for t in models
            ],
            "total": total,
        }

    def update_admin_ticket(self, ticket_id: str, data: dict) -> Dict[str, Any]:
        ticket = self.repo.get_by_id(ticket_id)
        if not ticket:
            raise SupportException.not_found()
        for field in ['status', 'priority', 'category']:
            if field in data:
                setattr(ticket, field, data[field])
        saved = self.repo.save(ticket)
        return SupportControllerMapper.to_response(saved)
