from django.conf import LazySettings
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

from neoviso_be.response import Response

settings = LazySettings()


class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        excluded_urls = [reverse('token_obtain_pair'), reverse('token_refresh')]
        if request.path not in excluded_urls:
            authenticator = JWTAuthentication()
            try:
                response = authenticator.authenticate(request)
                if response is not None:
                    user, token = response
                    request.user = user
                else:
                    raise InvalidToken
            except InvalidToken as e:
                return JsonResponse(Response(message='Unauthorized').__dict__, status=401)
