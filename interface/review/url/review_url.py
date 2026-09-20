from django.urls import path
from interface.review.view.review_view import ReviewListView, ReviewDetailView

urlpatterns = [
    path('reviews/', ReviewListView.as_view(), name='review-list'),
    path('reviews/<str:review_id>/', ReviewDetailView.as_view(), name='review-detail'),
]
