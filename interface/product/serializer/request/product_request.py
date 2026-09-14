from rest_framework import serializers


class ProductRequest(serializers.Serializer):
    store_id = serializers.CharField(max_length=36)
    category_id = serializers.CharField(max_length=36, required=False, allow_null=True, allow_blank=True)
    name = serializers.CharField(max_length=255)
    slug = serializers.SlugField(max_length=255)
    description = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    base_price = serializers.DecimalField(max_digits=12, decimal_places=2)
    compare_at_price = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    currency = serializers.CharField(max_length=3, default='USD', required=False)
    sku = serializers.CharField(max_length=100, required=False, allow_null=True, allow_blank=True)
    status = serializers.ChoiceField(
        choices=['draft', 'active', 'inactive', 'out_of_stock'],
        default='draft',
        required=False,
    )


class ProductPartialRequest(serializers.Serializer):
    category_id = serializers.CharField(max_length=36, required=False, allow_null=True, allow_blank=True)
    name = serializers.CharField(max_length=255, required=False)
    slug = serializers.SlugField(max_length=255, required=False)
    description = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    base_price = serializers.DecimalField(max_digits=12, decimal_places=2, required=False)
    compare_at_price = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    currency = serializers.CharField(max_length=3, required=False)
    sku = serializers.CharField(max_length=100, required=False, allow_null=True, allow_blank=True)
    status = serializers.ChoiceField(
        choices=['draft', 'active', 'inactive', 'out_of_stock'],
        required=False,
    )
