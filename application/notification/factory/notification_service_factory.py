from application.notification.notification_service_facade import NotificationServiceFacade
from domain.notification.service.notification_service import NotificationServiceInterface
from infrastructure.persistence.repository.notification_repository_impl import NotificationRepositoryInterfaceImpl


def notification_service_factory() -> NotificationServiceInterface:
    repo = NotificationRepositoryInterfaceImpl()
    return NotificationServiceFacade(repo)
