from utility.customized_response import response
from utility.error_msg import ErrorMsg, Error
from utility.customized_auth import Authentication
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from .serializer import LoginSerializer, RegisterSerializer, PermissionSerializer
from django.contrib.auth.hashers import check_password, make_password
from .models import Member, MemberPermission
import jwt
import os


class Login(APIView):
    parser_classes = (JSONParser,)

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
            secret = os.getenv("JWT_SECRET")
            jwt_token = jwt.encode({"user_id": user.member_id, "account": account}, secret, algorithm="HS256")
            return response(data={"jwt_token": jwt_token})
        else:
            raise Error(ErrorMsg.UNAUTHORIZED, 'Login Fail')


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
        user = Member.objects.filter(account=account).first()
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
    # permission_classes = [Authentication]

    def post(self, request):
        """
        PermissionSetting
        """
        register_check = PermissionSerializer(data=request.data)
        if not register_check.is_valid():
            raise Error(ErrorMsg.BAD_REQUEST)

        # register_check.save()

        return response()

    def get(self, request):
        member = MemberPermission.objects.select_related('user').all()
        if not member:
            raise Error(ErrorMsg.NOT_FOUND)

        data = PermissionSerializer(member, many=True).data

        return response(data=data)
