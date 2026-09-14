from rest_framework import serializers


class StoreRequest(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    slug = serializers.SlugField(max_length=255)
    owner_id = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    description = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    logo_url = serializers.URLField(required=False, allow_null=True, allow_blank=True)
    banner_url = serializers.URLField(required=False, allow_null=True, allow_blank=True)
    status = serializers.ChoiceField(
        choices=["active", "inactive", "suspended"],
        default="active",
        required=False,
    )


class StorePartialRequest(serializers.Serializer):
    name = serializers.CharField(max_length=255, required=False)
    slug = serializers.SlugField(max_length=255, required=False)
    owner_id = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    description = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    logo_url = serializers.URLField(required=False, allow_null=True, allow_blank=True)
    banner_url = serializers.URLField(required=False, allow_null=True, allow_blank=True)
    status = serializers.ChoiceField(
        choices=["active", "inactive", "suspended"],
        required=False,
    )
