from utility.customized_response import response
from utility.error_msg import ErrorMsg, Error
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from .serializer import LoginSerializer, RegisterSerializer
from django.contrib.auth.hashers import check_password, make_password
from .models import Member
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
            return response()
        account = check.validated_data.get('account')
        password = check.validated_data.get('password')
        user = Member.objects.filter(account=account).first()
        check = check_password(password, user.password)
        if check:
            secret = os.getenv("JWT_SECRET")
            jwt.encode({"user_id": user.member_id, "account": account}, secret, algorithm="HS256")
            return response()


class Register(APIView):
    parser_classes = (JSONParser,)

    def post(self, request):
        """
        Register
        """
        register_check = RegisterSerializer(data=request.data)
        if not register_check.is_valid():
            return response()
        account = register_check.validated_data.get('account')
        password = register_check.validated_data.get('password')
        user = Member.objects.filter(account=account).first()
        if user:
            raise Error(ErrorMsg.BAD_REQUEST, 'user_exist')

        register_check.validated_data.update({'password': make_password(password)})
        register_check.save()
        secret = os.getenv("JWT_SECRET")
        token = jwt.encode({"user_id": user.member_id, "account": account}, secret, algorithm="HS256")
        data = {
            'token': token
        }
        return response(data=data)
