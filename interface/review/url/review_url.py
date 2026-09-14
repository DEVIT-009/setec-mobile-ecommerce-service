from django.urls import path
from interface.review.view.review_view import ReviewListView, ReviewDetailView

urlpatterns = [
    path('', ReviewListView.as_view(), name='review-list'),
    path('<uuid:review_id>/', ReviewDetailView.as_view(), name='review-detail'),
]
