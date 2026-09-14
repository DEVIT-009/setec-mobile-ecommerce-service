from rest_framework import serializers


class TagRequest(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    slug = serializers.SlugField(max_length=120)


class TagPartialRequest(serializers.Serializer):
    name = serializers.CharField(max_length=100, required=False)
    slug = serializers.SlugField(max_length=120, required=False)
