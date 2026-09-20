from rest_framework import serializers


class CartItemRequest(serializers.Serializer):
    product_id = serializers.CharField()
    product_variant_id = serializers.CharField(required=False, allow_null=True)
    quantity = serializers.IntegerField(min_value=1, default=1)


class CartItemUpdateRequest(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1, required=False)
    is_selected = serializers.BooleanField(required=False)


class SelectAllRequest(serializers.Serializer):
    selected = serializers.BooleanField(default=True)


class CheckoutPreviewRequest(serializers.Serializer):
    shipping_address_id = serializers.CharField(required=False, allow_null=True)


# Backward-compatibility aliases
CartItemSerializer = CartItemRequest
CartItemUpdateSerializer = CartItemUpdateRequest
SelectAllSerializer = SelectAllRequest
CheckoutPreviewSerializer = CheckoutPreviewRequest
