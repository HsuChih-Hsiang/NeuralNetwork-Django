import json
import copy
from enum import Enum, unique
from rest_framework.exceptions import APIException

ERROR_CODE_LIST = {
    200: None,
    400: 'BAD_REQUEST',
    401: 'UNAUTHORIZED',
    404: 'NOT_FOUND',
    500: 'INTERNAL_SERVER_ERROR',
}


@unique
class ErrorMsg(Enum):
    OK = 200
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500


class Error(APIException):
    global ERROR_CODE_LIST

    def __init__(self, err: ErrorMsg, addition_msg: str = None):
        self.error = err
        self.addition_msg = addition_msg

    def getMessage(self):
        if not self.addition_msg:
            return ERROR_CODE_LIST[self.error.value]
        else:
            e = copy.deepcopy(ERROR_CODE_LIST[self.error.value])
            e += ", %s" % self.addition_msg
            return e

    def __str__(self):
        if not self.addition_msg:
            return json.dumps(ERROR_CODE_LIST[self.error.value], ensure_ascii=True, indent=4)
        else:
            e = copy.deepcopy(ERROR_CODE_LIST[self.error.value])
            e += ", %s" % self.addition_msg
            return json.dumps(e, ensure_ascii=True, indent=4)
