import jwt
import logging
from django.conf import settings
from django.core.cache import cache
from django.db.models import Q
from member.models import Member
from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import BasePermission
from utility.error_msg import Error, ErrorMsg

logger = logging.getLogger(__name__)


def parse_jwt(request, secret):
    jwt_tkn = request.META.get('HTTP_AUTHORIZATION')
    if not jwt_tkn:
        raise Error(ErrorMsg.UNAUTHORIZED, 'NOT_LOGIN')
    try:
        auth = jwt_tkn.split(' ')
        if len(auth) != 2:
            raise Error(ErrorMsg.UNAUTHORIZED, 'NOT_ACCEPT_TOKEN')
        authTkn = auth[1]
        res = jwt.decode(authTkn, secret, algorithms='HS256')

    except jwt.ExpiredSignatureError:
        raise Error(ErrorMsg.UNAUTHORIZED, 'JWT_TIME_OUT')
    except jwt.InvalidSignatureError:
        raise Error(ErrorMsg.UNAUTHORIZED, 'JWT_INVALID')
    except Exception as je:
        logger.error(je)
        raise Error(ErrorMsg.UNAUTHORIZED, 'PARSE_JWT_ERROR')
    return res


class Authentication(BaseAuthentication):
    def authenticate(self, request):
        parsed_jwt = parse_jwt(request, settings.SECRET_KEY)
        user_id = parsed_jwt.get('user_id')
        key = f'nn-{user_id}'
        user = cache.get(key)
        if not user:
            member = Member.objects.filter(member_id=user_id).first()
            cache.set(key, user, timeout=6000)
            if not member:
                raise Error(ErrorMsg.NOT_FOUND)
        return user, parsed_jwt.get('role')


class AdminPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        member = Member.objects.select_related('member_id').filter(
            member_id=request.user.id, member_id__admin=True
        ).first()
        return True if not member else False


class ReadOnlyPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        member = Member.objects.select_related('member_id').filter(
            Q(member_id=request.user.id) & (Q(member_id__read_only=True) | Q(member_id__admin=True))
        ).first()
        return True if not member else False

