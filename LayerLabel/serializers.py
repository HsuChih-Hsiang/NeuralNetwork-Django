from rest_framework import serializers
from .models import Topic, Subtopic, ModelClass, ModelDetails
from utility.error_msg import ErrorMsg, Error


class TopicCreateSerializer(serializers.Serializer):
    layer_id = serializers.IntegerField(read_only=True, source='id')
    name = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    is_show = serializers.BooleanField(required=False, write_only=True, default=True)
    description = serializers.CharField(required=False, write_only=True)
    is_description = serializers.SerializerMethodField(read_only=True)
    layer = serializers.SerializerMethodField(read_only=True)

    def get_is_description(self, obj):
        description = obj.description
        return True if description else False

    def get_layer(self, obj):
        if self.context == 'topic':
            return 1

        elif self.context == 'subtopic':
            return 2

        elif self.context == 'class':
            return 3

        elif self.context == 'detail':
            return 4

        else:
            raise Error(ErrorMsg.INTERNAL_SERVER_ERROR)

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


class SubtopicCreateSerializer(TopicCreateSerializer):

    def create(self, validated_data):
        subtopic = Subtopic.objects.create(**validated_data)
        return subtopic


class ModelClassCreateSerializer(TopicCreateSerializer):

    def create(self, validated_data):
        model_class = ModelClass.objects.create(**validated_data)
        return model_class


class ModelDetailsCreateSerializer(TopicCreateSerializer):

    def create(self, validated_data):
        model_detail = ModelDetails.objects.create(**validated_data)
        return model_detail
