from rest_framework import serializers


class VariantOptionRequest(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    value = serializers.CharField(max_length=100)


class ProductVariantRequest(serializers.Serializer):
    product_id = serializers.CharField()
    name = serializers.CharField(max_length=255)
    sku = serializers.CharField(max_length=100, required=False, allow_null=True, allow_blank=True)
    price = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    stock_quantity = serializers.IntegerField(default=0, required=False)
    status = serializers.ChoiceField(
        choices=['active', 'inactive', 'out_of_stock'],
        default='active',
        required=False,
    )
    options = VariantOptionRequest(many=True, required=False, default=list)


class ProductVariantPartialRequest(serializers.Serializer):
    name = serializers.CharField(max_length=255, required=False)
    sku = serializers.CharField(max_length=100, required=False, allow_null=True, allow_blank=True)
    price = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    stock_quantity = serializers.IntegerField(required=False)
    status = serializers.ChoiceField(
        choices=['active', 'inactive', 'out_of_stock'],
        required=False,
    )
    options = VariantOptionRequest(many=True, required=False)
