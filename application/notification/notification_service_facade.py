from typing import Dict, Any
from domain.notification.ports.notification_repository import NotificationRepositoryInterface
from domain.notification.service.notification_service import NotificationServiceInterface
from domain.notification.entity.notification import Notification
from domain.notification.exception.notification_exception import NotificationException
from interface.notification.serializer.mapper.notification_controller_mapper import NotificationControllerMapper


class NotificationServiceFacade(NotificationServiceInterface):

    def __init__(self, repo: NotificationRepositoryInterface):
        self.repo = repo

    def list(self, user_id: str, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        notifications, total = self.repo.list_by_user(user_id, page, page_size)
        return {
            "items": NotificationControllerMapper.to_list_response(notifications),
            "total": total,
        }

    def unread_count(self, user_id: str) -> Dict[str, Any]:
        count = self.repo.unread_count(user_id)
        return {"unread_count": count}

    def mark_read(self, user_id: str, notification_id: str) -> None:
        self.repo.mark_read(notification_id, user_id)

    def mark_all_read(self, user_id: str) -> None:
        self.repo.mark_all_read(user_id)

    def delete(self, user_id: str, notification_id: str) -> None:
        self.repo.soft_delete(notification_id, user_id)

    def create_admin_notification(self, data: dict) -> Dict[str, Any]:
        from infrastructure.persistence.models.notification_model import Notification as NotificationModel
        notif = NotificationModel.objects.create(
            user_id=data['user_id'],
            type=data['type'],
            title=data['title'],
            body=data.get('body'),
            data=data.get('data'),
            status='sent',
        )
        return {
            "id": str(notif.id),
            "user_id": str(notif.user_id),
            "type": notif.type,
            "title": notif.title,
            "status": notif.status,
            "created_at": notif.created_at.isoformat(),
        }
