from application.support_ticket.support_ticket_service_facade import SupportTicketServiceFacade
from domain.support_ticket.service.support_service import SupportServiceInterface
from infrastructure.persistence.repository.support_repository_impl import SupportRepositoryInterfaceImpl


def support_ticket_service_factory() -> SupportServiceInterface:
    repo = SupportRepositoryInterfaceImpl()
    return SupportTicketServiceFacade(repo)
