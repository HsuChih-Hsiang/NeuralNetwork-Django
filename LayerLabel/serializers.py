from rest_framework import serializers
from .models import Topic, Subtopic, ModelClass, ModelDetails
from utility.error_msg import ErrorMsg, Error


class TopicCreateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, write_only=True, allow_null=False, allow_blank=False)
    is_description = serializers.SerializerMethodField(read_only=True)

    def get_is_description(self, obj):
        description = obj.description
        return True if description else False

    def create(self, validated_data):
        topic = Topic.objects.create(**validated_data)
        return topic


class SearchTextSerializer(serializers.Serializer):
    search_txt = serializers.CharField(required=False, write_only=True, allow_null=False, allow_blank=False)
