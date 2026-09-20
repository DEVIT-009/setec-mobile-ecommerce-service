from django.urls import path
from interface.user.view.user_view import (
    UserMeView, UserProfileView, UserSecurityView,
    UserSessionsView, UserSessionRevokeView,
)
from interface.review.view.review_view import UserReviewListView
from interface.legal_document.view.legal_document_view import UserLegalAcceptancesView

urlpatterns = [
    path('me/', UserMeView.as_view(), name='user-me'),
    path('me/profile/', UserProfileView.as_view(), name='user-profile'),
    path('me/security-settings/', UserSecurityView.as_view(), name='user-security'),
    path('me/sessions/', UserSessionsView.as_view(), name='user-sessions'),
    path('me/sessions/<str:session_id>/', UserSessionRevokeView.as_view(), name='user-session-delete'),
    path('me/sessions/<str:session_id>/revoke/', UserSessionRevokeView.as_view(), name='user-session-revoke'),
    path('me/reviews/', UserReviewListView.as_view(), name='user-reviews'),
    path('me/legal-acceptances/', UserLegalAcceptancesView.as_view(), name='user-legal-acceptances'),
]
