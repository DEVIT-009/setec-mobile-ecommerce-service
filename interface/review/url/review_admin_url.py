from django.urls import path
from interface.review.view.review_admin_view import AdminReviewListView, AdminReviewDetailView

# Admin review management endpoints — require authentication + admin role.
# GET    /api/v1/admin/reviews/
# GET    /api/v1/admin/reviews/<uuid:review_id>/
# PATCH  /api/v1/admin/reviews/<uuid:review_id>/
# DELETE /api/v1/admin/reviews/<uuid:review_id>/
urlpatterns = [
    path('reviews/', AdminReviewListView.as_view(), name='admin-review-list'),
    path('reviews/<uuid:review_id>/', AdminReviewDetailView.as_view(), name='admin-review-detail'),
]
