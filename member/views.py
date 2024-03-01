from utility.customized_response import response
from utility.error_msg import ErrorMsg, Error
from utility.customized_auth import AdminPermission, Authentication
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from .serializer import LoginSerializer, RegisterSerializer, PermissionSerializer, UpdatePermissionSerializer
from django.contrib.auth.hashers import check_password, make_password
from django.db.models import Q
from django.conf import settings
from .models import Member, MemberPermission
import jwt
import os


class Login(APIView):
    parser_classes = (JSONParser,)

    def get_authenticators(self):
        if self.request.method == 'GET':
            return (Authentication(),)
        return ()

    def get_permissions(self):
        if self.request.method == 'GET':
            return (AdminPermission(),)
        return ()

    def post(self, request):
        """
        Login
        """
        check = LoginSerializer(data=request.data)
        if not check.is_valid():
            raise Error(ErrorMsg.BAD_REQUEST, 'Bad Parameters')
        account = check.validated_data.get('account')
        password = check.validated_data.get('password')
        user = Member.objects.filter(account=account).first()
        check = check_password(password, user.password) if user else False

        if check:
            secret = settings.JWT_SECRET
            jwt_token = jwt.encode({"user_id": user.member_id, "account": account}, secret, algorithm="HS256")
            return response(data={"jwt_token": jwt_token})
        else:
            raise Error(ErrorMsg.UNAUTHORIZED, 'Login Fail')

    def get(self, user_id):
        member = Member.objects.filter(member_id=user_id).first()
        if not member:
            raise Error(ErrorMsg.UNAUTHORIZED)
        return True


class Register(APIView):
    parser_classes = (JSONParser,)

    def post(self, request):
        """
        Register
        """
        register_check = RegisterSerializer(data=request.data)
        if not register_check.is_valid():
            raise Error(ErrorMsg.BAD_REQUEST, 'user_exist')

        account = register_check.validated_data.get('account')
        password = register_check.validated_data.get('password')
        email = register_check.validated_data.get('email')

        user = Member.objects.filter(Q(account=account) | Q(email=email)).first()
        if user:
            raise Error(ErrorMsg.BAD_REQUEST, 'user_exist')

        register_check.validated_data.update({'password': make_password(password)})
        register_result = register_check.save()
        secret = os.getenv("JWT_SECRET")
        token = jwt.encode({"user_id": register_result.member_id, "account": account}, secret, algorithm="HS256")
        data = {
            'token': token
        }
        return response(data=data)


class Permission(APIView):
    parser_classes = (JSONParser,)
    authentication_classes = (Authentication,)
    permission_classes = (AdminPermission,)

    def post(self, request):
        """
        PermissionSetting
        """
        permission = UpdatePermissionSerializer(data=request.data)
        if not permission.is_valid():
            raise Error(ErrorMsg.BAD_REQUEST)

        permission_data = permission.validated_data.get('permission_data')

        for data in permission_data:
            user_id = data.pop('user_id')
            read_only = data.get('read_only')
            admin = data.get('admin')
            name = data.get('name')
            email = data.get('email')

            member_permission = MemberPermission.objects.filter(user=user_id)
            member = Member.objects.filter(member_id=user_id)
            if member:
                member.update(name=name, email=email)
            if not member_permission:
                raise Error(ErrorMsg.BAD_REQUEST, 'member not exist')
            if admin:
                member_permission.update(read_only=True, admin=True)
            else:
                admin_num = MemberPermission.objects.filter(admin=True).count()
                member_admin = member_permission.first().admin
                if admin_num <= 1 and member_admin:
                    raise Error(ErrorMsg.BAD_REQUEST, 'will not exist admin')
                else:
                    member_permission.update(read_only=read_only, admin=admin)

        member_data = MemberPermission.objects.select_related('user').order_by('user').all()
        data = PermissionSerializer(member_data, many=True).data
        return response(data=data)

    def get(self, request):
        member = MemberPermission.objects.select_related('user').order_by('user').all()
        if not member:
            raise Error(ErrorMsg.NOT_FOUND)

        data = PermissionSerializer(member, many=True).data

        return response(data=data)
