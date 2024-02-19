import logging
import traceback
from rest_framework.response import Response
from rest_framework import exceptions
from utility.error_msg import ErrorMsg, Error

logger = logging.getLogger(__name__)


def response(error_code: ErrorMsg = ErrorMsg.OK, data: dict | list = None):
    error_msg = Error(error_code).getMessage()
    res_data = {
        'errorMsg': error_msg,
        'result': data if data is not None else dict()
    }
    return Response(res_data, status=error_code.value)


def custom_exception_handler(exc: Exception, context):
    if isinstance(exc, Error):
        err_msg = exc.getMessage()
        err_code = exc.error.value
    elif isinstance(exc, exceptions.ParseError):
        err_msg = 'JSON_FORMAT_ERROR'
        err_code = 520
    else:
        err_msg = 'INTERNAL_SERVER_ERROR'
        err_code = 500
    data = {
        'errorMsg': err_msg,
        'errorCode': err_code,
    }
    logger.error(traceback.format_exc())
    logger.error(exc)
    res = Response(data=data, status=err_code)
    return res
