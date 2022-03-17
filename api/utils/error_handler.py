import json
import traceback

from django.conf import settings
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError, APIException
from rest_framework.response import Response
from rest_framework.views import exception_handler

from .errors import ERRORS, Error


# noinspection PyAbstractClass
class ErrorSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)
    message = serializers.CharField(required=True)


class WrapperException(APIException):

    def __init__(self, error_code: object, error_message: object = None, namespace: object = None,
                 status_code: object = status.HTTP_400_BAD_REQUEST,
                 errors: object = [], origin_exception: object = None) -> object:
        if origin_exception:
            self.error_code = self._camel_case_error_code(type(origin_exception).__name__)
            self.error_message = str(origin_exception)
        else:
            self.error_code = error_code
            # setting attribute detail from inherited class APIException
            self.error_message = self.detail = error_message
        self.namespace = namespace
        self.errors = errors
        self.status_code = status_code

    def __str__(self):
        return self.error_message if self.error_message is not None else self.error_code

    def _camel_case_error_code(self, msg):
        if not msg:
            return ''
        out = ''
        if msg[0].isupper():
            out = msg[:1].lower()
        else:
            return msg
        for idx, c in enumerate(msg[1:], start=1):
            if c.isupper() and msg[idx + 1].isupper():
                out += msg[idx].lower()
            else:
                out += msg[idx:]
                break
        return out


camelCase = lambda s: s[:1].lower() + s[1:] if s else ''


def add_err_message(grouped_err, key, value):
    if key in grouped_err:
        grouped_err[key].append(value)
    else:
        grouped_err[key] = [value]


def format_field_name(base_field, field, index=None):
    if base_field:
        return "{}.{}".format(base_field, field)
    elif index is not None:
        return "{}.{}".format(field, index)
    else:
        return field


def filter_messages(items, base_field=None):
    grouped_err = {}

    if isinstance(items, dict):
        items = items.items()

    for field, details in items:
        if isinstance(details, dict):
            sub_groups = filter_messages(details.items(), format_field_name(base_field, field))
            for detail, sub_group_names in sub_groups.items():
                for sub_group in sub_group_names:
                    add_err_message(grouped_err, detail, sub_group)
        elif isinstance(details, list):
            sub_groups = {}
            for idx, detail in enumerate(details):
                if "message" in detail:
                    detail = detail['message'].capitalize()
                    add_err_message(grouped_err, detail, format_field_name(base_field, field))
                else:
                    sub_groups = filter_messages(detail, format_field_name(base_field, field, idx))
                    for detail, sub_group_names in sub_groups.items():
                        for sub_group in sub_group_names:
                            add_err_message(grouped_err, detail, sub_group)

    return grouped_err


def custom_exception_handler(exc: Exception, context):
    response = exception_handler(exc, context)

    if response is None:
        status_code = 500
    else:
        status_code = response.status_code
    traceback.print_exception(type(exc), exc, exc.__traceback__)

    if isinstance(exc, ValidationError):
        grouped_err = filter_messages(exc.get_full_details().items())
        error_message = []
        for x in grouped_err:
            error_message.append({'fields': grouped_err[x], 'reason': x})
        return Response(ErrorSerializer(Error('validationError', json.dumps(error_message))).data,
                        status.HTTP_400_BAD_REQUEST)
    elif isinstance(exc, WrapperException):
        if exc.status_code:
            status_code = exc.status_code
        error_response = __get_error_from_code(exc.error_code, status_code, exc.error_message)
        if error_response is None:
            if exc.error_message is None and settings.DEBUG:
                return Response(ErrorSerializer("assertionError",
                                                "%s is not added to ERROR_OBJECT constant! Check ERROR_OBJECTS in apiv2/constants/error.py" % exc.error_code).data,
                                status_code)
            return Response(ErrorSerializer(Error(exc.error_code, exc.error_message)).data, status_code)
        return error_response

    return Response(ErrorSerializer(Error(camelCase(type(exc).__name__), str(exc))).data, status_code,
                    headers={v[0]: v[1] for k, v in (response._headers.items() if response else {})})


def __get_error_from_code(error_code, status_code, error_message):
    if error_code in ERRORS:
        error = ERRORS.get(error_code)

        if status_code is None:
            status_code = error.http_status_code
        if error_message is not None:
            error.message = error_message
        return Response(ErrorSerializer(error).data, status_code)
    return None
