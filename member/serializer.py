from rest_framework import serializers
from .models import Member, MemberPermission


class LoginSerializer(serializers.Serializer):
    account = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    password = serializers.CharField(required=True, allow_null=False, allow_blank=False)


class RegisterSerializer(serializers.Serializer):
    account = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    password = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    name = serializers.CharField(required=True, allow_null=False, allow_blank=False)

    def create(self, validated_data):
        user = Member.objects.create(**validated_data)
        member_num = Member.objects.count()
        if user and member_num <= 1:
            MemberPermission.objects.create(member_id=user.id, admin=True)
        elif user:
            MemberPermission.objects.create(member_id=user.id)

