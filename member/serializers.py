from rest_framework import serializers
from .models import Member, MemberPermission
from utility.error_msg import ErrorMsg, Error


class LoginSerializer(serializers.Serializer):
    account = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    password = serializers.CharField(required=True, allow_null=False, allow_blank=False)


class RegisterSerializer(serializers.Serializer):
    account = serializers.CharField(required=True, allow_null=False, allow_blank=False, min_length=8)
    password = serializers.RegexField(required=True, regex=r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$')
    name = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    email = serializers.EmailField(required=True, allow_null=False, allow_blank=False)

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
    user_id = serializers.IntegerField(source='user.member_id')
    account = serializers.CharField(source='user.account')
    name = serializers.CharField(source='user.name')
    email = serializers.SerializerMethodField()
    admin = serializers.BooleanField()
    read_only = serializers.BooleanField()

    def get_email(self, obj):
        email = obj.user.email
        return email if email else str()


class PermissionDictField(serializers.DictField):
    user_id = serializers.IntegerField(required=True, allow_null=False)
    name = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    admin = serializers.BooleanField(required=True, allow_null=False)
    read_only = serializers.BooleanField(required=True, allow_null=False)


class UpdatePermissionSerializer(serializers.Serializer):
    permission_data = serializers.ListField(child=PermissionDictField())
