import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser, Group
from rest_framework.authentication import (BaseAuthentication,
                                           get_authorization_header)

logger = logging.getLogger(__name__)


class FederationAuthentication(BaseAuthentication):
    def authenticate(self, request):
        user = {}
        if not request.META.get('HTTP_X_USER_ID', None):
            return AnonymousUser()
        user["id"] = request.META['HTTP_X_USER_ID']
        user["first_name"] = request.META['HTTP_X_USER_FIRSTNAME']
        user["last_name"] = request.META['HTTP_X_USER_LASTNAME']
        user["email"] = request.META['HTTP_X_USER_EMAIL']
        user, _ = get_user_model().objects.get_or_create(
            username=user["email"],
            defaults=user,
        )
        group = user.groups.all().first()
        if not group:
            group, _ = Group.objects.get_or_create(
                name=request.META['HTTP_X_USER_GROUP']
            )
            user.groups.set([group])
            user.save()
        return user, group
