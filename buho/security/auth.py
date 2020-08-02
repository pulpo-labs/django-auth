import logging

from django.contrib.auth import get_user_model
from rest_framework.authentication import get_authorization_header, BaseAuthentication
from django.conf import settings


logger = logging.getLogger(__name__)


class FederationAuthentication(BaseAuthentication):
    def authenticate(self, request):
        user = {}
        user["id"] = request.META['X-User-Id']
        user["first_name"] = request.META['X-User-FirstName']
        user["last_name"] = request.META.get['X-User-LastName']
        user["phone"] = request.META.get['X-User-Phone']
        user["email"] = request.META.get['X-User-Email']

        user, __ = get_user_model().objects.get_or_create(
            username=user["email"],
            defaults=user,
        )

        return user
