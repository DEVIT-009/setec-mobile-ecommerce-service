from rest_framework import serializers


class SearchHistoryRecordRequest(serializers.Serializer):
    query = serializers.CharField(max_length=500)
    filters_json = serializers.JSONField(required=False, allow_null=True)
    result_count = serializers.IntegerField(required=False, allow_null=True)


# Backward-compatibility alias
SearchHistoryRecordSerializer = SearchHistoryRecordRequest
