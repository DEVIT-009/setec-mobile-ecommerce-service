from django.urls import path
from interface.support_ticket.view.support_ticket_admin_view import (
    AdminSupportTicketListView,
    AdminSupportTicketDetailView,
    AdminSupportTicketReplyView,
)

# Admin support ticket management endpoints — require authentication + admin role.
# GET   /api/v1/admin/support/tickets/
# GET   /api/v1/admin/support/tickets/<uuid:ticket_id>/
# PATCH /api/v1/admin/support/tickets/<uuid:ticket_id>/
# POST  /api/v1/admin/support/tickets/<uuid:ticket_id>/messages/
urlpatterns = [
    path('support/tickets/', AdminSupportTicketListView.as_view(), name='admin-support-ticket-list'),
    path('support/tickets/<uuid:ticket_id>/', AdminSupportTicketDetailView.as_view(), name='admin-support-ticket-detail'),
    path('support/tickets/<uuid:ticket_id>/messages/', AdminSupportTicketReplyView.as_view(), name='admin-support-ticket-reply'),
]
