import logging

from django.contrib.auth import get_user_model
from rest_framework.authentication import get_authorization_header, BaseAuthentication
from django.conf import settings


logger = logging.getLogger(__name__)


class FederationAuthentication(BaseAuthentication):
    def authenticate(self, request):
        user = {}
        user["id"] = request.META['HTTP_X_USER_ID']
        user["first_name"] = request.META['HTTP_X_USER_FIRSTNAME']
        user["last_name"] = request.META['HTTP_X_USER_LASTNAME']
        user["email"] = request.META['HTTP_X_USER_EMAIL']
        user, __ = get_user_model().objects.get_or_create(
            username=user["email"],
            defaults=user,
        )
        return user
