from rest_framework import serializers

ORDER_STATUS_CHOICES = [
    'pending', 'confirmed', 'processing', 'shipped', 'delivered',
    'cancelled', 'refunded', 'failed',
]


class PlaceOrderRequest(serializers.Serializer):
    cart_id = serializers.CharField()
    shipping_address_id = serializers.CharField()
    idempotency_key = serializers.CharField(max_length=128)


class AdminOrderUpdateStatusRequest(serializers.Serializer):
    status = serializers.ChoiceField(choices=ORDER_STATUS_CHOICES)
    note = serializers.CharField(required=False, allow_blank=True)


# Backward-compatibility aliases
PlaceOrderSerializer = PlaceOrderRequest
AdminOrderUpdateStatusSerializer = AdminOrderUpdateStatusRequest
