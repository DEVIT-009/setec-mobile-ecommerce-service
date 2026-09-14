from typing import Dict, Any, List
from dataclasses import asdict
from domain.notification.entity.notification import Notification
from interface.notification.serializer.response.notification_response import NotificationResponse


class NotificationControllerMapper:

    @staticmethod
    def to_response(notification: Notification) -> Dict[str, Any]:
        response_dto = NotificationResponse(
            id=str(notification.id) if notification.id else None,
            type=notification.type,
            title=notification.title,
            body=notification.body,
            data=notification.data,
            read_at=notification.read_at.isoformat() if notification.read_at else None,
            status=notification.status,
            created_at=notification.created_at.isoformat() if notification.created_at else None,
        )
        return asdict(response_dto)

    @staticmethod
    def to_list_response(notifications: List[Notification]) -> List[Dict[str, Any]]:
        return [NotificationControllerMapper.to_response(n) for n in notifications]

