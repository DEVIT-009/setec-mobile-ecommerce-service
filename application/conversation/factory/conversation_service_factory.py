from application.conversation.conversation_service_facade import ConversationServiceFacade
from domain.conversation.service.conversation_service import ConversationServiceInterface
from infrastructure.persistence.repository.conversation_repository_impl import ConversationRepositoryInterfaceImpl


def conversation_service_factory() -> ConversationServiceInterface:
    repo = ConversationRepositoryInterfaceImpl()
    return ConversationServiceFacade(repo)
