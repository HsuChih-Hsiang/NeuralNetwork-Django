from rest_framework import serializers
from .models import Member


class LoginSerializer(serializers.Serializer):
    account = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    password = serializers.CharField(required=True, allow_null=False, allow_blank=False)


class RegisterSerializer(serializers.Serializer):
    account = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    password = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    name = serializers.CharField(required=True, allow_null=False, allow_blank=False)

    def create(self, validated_data):
        Member.objects.create(**validated_data)
