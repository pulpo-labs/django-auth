from rest_framework.exceptions import APIException
from rest_framework import status


class UserInfoRetrievalFailed(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'An error happened while trying to retrieve the user information.'
    default_code = 'jwt_authentication_failure'


class UserNotAuthenticated(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'User not authenticated.'
    default_code = 'auth_service_response_failure'
