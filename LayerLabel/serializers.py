from rest_framework import serializers
from .models import Topic, Subtopic, ModelClass, ModelDetails
from utility.error_msg import ErrorMsg, Error


class TopicCreateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, write_only=True, allow_null=False, allow_blank=False)
    is_show = serializers.BooleanField(required=False, write_only=True, default=True)
    description = serializers.CharField(required=False, write_only=True)
    is_description = serializers.SerializerMethodField(read_only=True)

    def get_is_description(self, obj):
        description = obj.description
        return True if description else False

    def create(self, validated_data):
        topic = Topic.objects.create(**validated_data)
        return topic

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.is_show = validated_data.get('is_show', instance.is_show)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance


class SearchTextSerializer(serializers.Serializer):
    search_txt = serializers.CharField(required=False, write_only=True, allow_null=False, allow_blank=False)
