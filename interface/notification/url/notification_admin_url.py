from django.urls import path
from interface.notification.view.notification_admin_view import AdminNotificationListView

# Admin notification management endpoints — require authentication + admin role.
# GET  /api/v1/admin/notifications/
# POST /api/v1/admin/notifications/
urlpatterns = [
    path('notifications/', AdminNotificationListView.as_view(), name='admin-notification-list'),
]
