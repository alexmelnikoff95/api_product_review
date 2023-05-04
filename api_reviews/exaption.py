from rest_framework import status
from rest_framework.exceptions import APIException


class APIReviewException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class MyException(Exception):
    pass


