from django.urls import path
from interface.cart.view.cart_view import (
    CartView, CartItemListView, CartItemDetailView,
    CartSelectAllView, CartCheckoutPreviewView,
)

urlpatterns = [
    path('', CartView.as_view(), name='cart-get'),
    path('items/', CartItemListView.as_view(), name='cart-items'),
    path('items/<str:cart_item_id>/', CartItemDetailView.as_view(), name='cart-item-detail'),
    path('select-all/', CartSelectAllView.as_view(), name='cart-select-all'),
    path('checkout-preview/', CartCheckoutPreviewView.as_view(), name='cart-checkout-preview'),
]
