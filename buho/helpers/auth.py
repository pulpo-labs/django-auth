import logging

from .exceptions import UserNotAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.authentication import get_authorization_header, BaseAuthentication
from django.conf import settings


logger = logging.getLogger(__name__)


class BearerAuthentication(BaseAuthentication):
    """
    Simple token based authentication.
    This authentication class is useful for authenticating an OAuth2 access token against a remote
    authentication provider. Clients should authenticate by passing the token key in the "Authorization" HTTP header,
    prepended with the string `"Bearer "`.
    This class relies on the JWT_VALIDATION_URL being set to the value of an endpoint on the OAuth provider, that
    returns a JSON object with information about the user. See ``process_user_info_response`` for the expected format
    of this object. This data will be used to get, or create, a ``User``. Additionally, it is assumed that a successful
    response from this endpoint (authenticated with the provided access token) implies the access token is valid.
    Example Header:
        Authorization: Bearer 401f7ac837da42b97f613d789819ff93537bee6a
    """
    def authenticate(self, request):
        # if not self.get_user_info_url():
        #     logger.warning('The setting JWT_VALIDATION_URL is invalid!')
        #     raise AuthServiceResponseFailed()
        user = {}
        try: 
            user["id"] = request.META['X-User-Id']
            user["first_name"] = request.META['X-User-FirstName']
            user["last_name"] = request.META.get['X-User-LastName']
            user["phone"] = request.META.get['X-User-Phone']            
            user["email"] = request.META.get['X-User-Email']
        except KeyError:    
            raise UserNotAuthenticated("One or more keys empty from authentication.")

        user, __ = get_user_model().objects.get_or_create(
            username=user["email"], 
            defaults=user,
        )

        return user
