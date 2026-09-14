from typing import List, Optional, Tuple
from django.utils import timezone
from domain.notification.ports.notification_repository import NotificationRepositoryInterface
from domain.notification.entity.notification import Notification
from infrastructure.persistence.mapper.notification_persistence_mapper import NotificationPersistenceMapper
from infrastructure.persistence.models.notification_model import Notification as NotificationModel


class NotificationRepositoryInterfaceImpl(NotificationRepositoryInterface):

    def list_by_user(self, user_id: str, page: int, page_size: int) -> Tuple[List[Notification], int]:
        qs = NotificationModel.objects.filter(user_id=user_id, deleted_at__isnull=True).order_by('-created_at')
        total = qs.count()
        offset = (page - 1) * page_size
        models = list(qs[offset:offset + page_size])
        return [NotificationPersistenceMapper.from_entity(m) for m in models if m is not None], total

    def unread_count(self, user_id: str) -> int:
        return NotificationModel.objects.filter(user_id=user_id, read_at__isnull=True, deleted_at__isnull=True).count()

    def mark_read(self, notification_id: str, user_id: str) -> None:
        NotificationModel.objects.filter(id=notification_id, user_id=user_id, read_at__isnull=True).update(read_at=timezone.now())

    def mark_all_read(self, user_id: str) -> None:
        NotificationModel.objects.filter(user_id=user_id, read_at__isnull=True, deleted_at__isnull=True).update(read_at=timezone.now())

    def soft_delete(self, notification_id: str, user_id: str) -> None:
        NotificationModel.objects.filter(id=notification_id, user_id=user_id).update(deleted_at=timezone.now())

    def get_by_id(self, notification_id: str, user_id: str) -> Optional[Notification]:
        model = NotificationModel.objects.filter(id=notification_id, user_id=user_id, deleted_at__isnull=True).first()
        if not model:
            return None
        return NotificationPersistenceMapper.from_entity(model)
