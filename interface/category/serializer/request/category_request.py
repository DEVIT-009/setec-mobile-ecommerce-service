from rest_framework import serializers


class CategoryRequest(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    slug = serializers.SlugField(max_length=255)
    parent_id = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    icon_url = serializers.URLField(required=False, allow_null=True, allow_blank=True)
    image_url = serializers.URLField(required=False, allow_null=True, allow_blank=True)
    sort_order = serializers.IntegerField(required=False, default=0)
    status = serializers.ChoiceField(
        choices=["active", "inactive"],
        default="active",
        required=False,
    )


class CategoryPartialRequest(serializers.Serializer):
    name = serializers.CharField(max_length=255, required=False)
    slug = serializers.SlugField(max_length=255, required=False)
    parent_id = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    icon_url = serializers.URLField(required=False, allow_null=True, allow_blank=True)
    image_url = serializers.URLField(required=False, allow_null=True, allow_blank=True)
    sort_order = serializers.IntegerField(required=False)
    status = serializers.ChoiceField(
        choices=["active", "inactive"],
        required=False,
    )

