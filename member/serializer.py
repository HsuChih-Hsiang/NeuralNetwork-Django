from rest_framework import serializers
from .models import Member, MemberPermission
from utility.error_msg import ErrorMsg, Error


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
            MemberPermission.objects.create(user=user, admin=True)
        elif user:
            MemberPermission.objects.create(user=user)
        else:
            raise Error(ErrorMsg.BAD_REQUEST, 'user_exist')

        return user


class PermissionSerializer(serializers.Serializer):
    member_id = serializers.IntegerField(required=True, allow_null=False, source='user.member_id')
    account = serializers.CharField(read_only=True, source='user.account')
    name = serializers.CharField(read_only=True, source='user.name')
    admin = serializers.BooleanField(required=False, allow_null=False)
    read_only = serializers.BooleanField(required=False, allow_null=False)



