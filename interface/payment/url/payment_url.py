from django.urls import path

from interface.payment.view.payment_view import OrderBatchPaymentView, OrderPaymentView


urlpatterns = [
    path('payment/', OrderBatchPaymentView.as_view(), name='order-batch-payment'),
    path('<str:order_id>/payment/', OrderPaymentView.as_view(), name='order-payment'),
]
