import json

from buho.security.auth import FederationAuthentication
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated

APOLLO_QUERY = '{"query":"query __ApolloGetServiceDefinition__ { _service { sdl } }"}'


class AuthenticatedGraphQLView(GraphQLView, FederationAuthentication):
    permission_classes = (IsAuthenticated,)

    def check_permissions(self, request):
        for permission_class in self.permission_classes:
            if not permission_class().has_permission(request, self):
                return False
        return True

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        if APOLLO_QUERY == request.body.decode('utf-8'):
            return super(AuthenticatedGraphQLView, self).dispatch(request, *args, **kwargs)
        try:
            user = self.authenticate(request)
            request.user = user
            # if user is None:
            #     return HttpResponse(
            #         json.dumps({
            #             'detail': 'You do not have permission to perform this action.',
            #             'status_code': status.HTTP_403_FORBIDDEN
            #         }),
            #         status=status.HTTP_403_FORBIDDEN,
            #         content_type='application/json'
            #     )
            # has_permission = self.check_permissions(request)
            # if not has_permission:
            #     return HttpResponse(
            #         json.dumps({
            #             'detail': 'You do not have permission to perform this action.',
            #             'status_code': status.HTTP_403_FORBIDDEN
            #         }),
            #         status=status.HTTP_403_FORBIDDEN,
            #         content_type='application/json'
            #     )
        except AuthenticationFailed:
            return HttpResponse(
                json.dumps({
                    'detail': 'Authentication credentials were not provided.',
                    'status_code': status.HTTP_401_UNAUTHORIZED
                }),
                status=status.HTTP_401_UNAUTHORIZED,
                content_type='application/json'
            )
        except KeyError:
            return HttpResponse(
                json.dumps({
                    'detail': 'Authentication headers not in place.',
                    'status_code': status.HTTP_401_UNAUTHORIZED
                }),
                status=status.HTTP_401_UNAUTHORIZED,
                content_type='application/json'
            )
        return super(AuthenticatedGraphQLView, self).dispatch(request, *args, **kwargs)
