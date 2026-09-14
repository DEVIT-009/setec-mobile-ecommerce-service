from typing import Optional
from domain.notification.entity.notification import Notification as DomainNotification
from infrastructure.persistence.models.notification_model import Notification as NotificationModel


class NotificationPersistenceMapper:

    @staticmethod
    def from_entity(entity: Optional[NotificationModel]) -> Optional[DomainNotification]:
        if entity is None:
            return None
        return DomainNotification(
            id=str(entity.id),
            user_id=str(entity.user_id) if entity.user_id else None,
            type=entity.type,
            title=entity.title,
            body=entity.body,
            data=entity.data,
            read_at=entity.read_at,
            status=entity.status,
            created_at=entity.created_at,
            deleted_at=entity.deleted_at,
        )

    @staticmethod
    def to_model(domain: DomainNotification, model_instance: Optional[NotificationModel] = None) -> NotificationModel:
        model = model_instance or NotificationModel()
        if domain.user_id:
            model.user_id = domain.user_id
        model.type = domain.type
        model.title = domain.title
        model.body = domain.body
        model.data = domain.data
        model.read_at = domain.read_at
        model.status = domain.status
        model.deleted_at = domain.deleted_at
        return model
