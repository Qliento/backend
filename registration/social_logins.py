# from rest_framework import generics, permissions, status
# from rest_framework.response import Response
# from requests.exceptions import HTTPError
# from social_django.utils import load_strategy, load_backend
# from social_core.backends.oauth import BaseOAuth2
# from social_core.exceptions import MissingBackend, AuthTokenError, AuthForbidden
# from . import serializers
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.contrib.auth import authenticate, login
# from .models import Users
#
#
# class SocialLoginView(generics.GenericAPIView):
#     """Log in using facebook"""
#     serializer_class = serializers.SocialSerializer
#     permission_classes = [permissions.AllowAny]
#
#     def post(self, request):
#         """Authenticate user through the provider and access_token"""
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         provider = serializer.data.get('provider', None)
#         strategy = load_strategy(request)
#
#         try:
#             backend = load_backend(strategy=strategy, name=provider,
#                                    redirect_uri=None)
#
#         except MissingBackend:
#             return Response({'error': 'Please provide a valid provider'},
#                             status=status.HTTP_400_BAD_REQUEST)
#         try:
#             access_token = None
#             if isinstance(backend, BaseOAuth2):
#                 access_token = serializer.data.get('access_token')
#             user = backend.do_auth(access_token)
#
#         except HTTPError as error:
#             return Response({
#                 "error": {
#                     "access_token": "Invalid token",
#                     "details": str(error)
#                 }
#             }, status=status.HTTP_400_BAD_REQUEST)
#         except AuthTokenError as error:
#             return Response({
#                 "error": "Invalid credentials",
#                 "details": str(error)
#             }, status=status.HTTP_400_BAD_REQUEST)
#
#         try:
#             authenticated_user = authenticate(request, username=user.email)
#             print(authenticated_user.is_active)
#         except HTTPError as error:
#             return Response({
#                 "error": "invalid token",
#                 "details": str(error)
#             }, status=status.HTTP_400_BAD_REQUEST)
#
#         except AuthForbidden as error:
#             return Response({
#                 "error": "invalid token",
#                 "details": str(error)
#             }, status=status.HTTP_400_BAD_REQUEST)
#
#         if authenticated_user and authenticated_user.is_active:
#             # generate JWT token
#
#             data = {
#                 "token": "{}".format(RefreshToken.for_user(user).access_token)}
#             # customize the response to your needs
#             response = {
#                 "email": authenticated_user.email,
#                 "token": data.get('token')
#             }
#             return Response(status=status.HTTP_200_OK, data=response)

from rest_framework.authentication import get_authorization_header
from rest_framework import exceptions, HTTP_HEADER_ENCODING
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework_social_oauth2.authentication import SocialAuthentication
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework import exceptions, HTTP_HEADER_ENCODING

from django.utils.translation import ugettext_lazy as _
from rest_framework import HTTP_HEADER_ENCODING, authentication

from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken, TokenError
from rest_framework_simplejwt.models import TokenUser
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.state import User

from collections import OrderedDict
from oauth2_provider.oauth2_backends import get_oauthlib_core


AUTH_HEADER_TYPES = api_settings.AUTH_HEADER_TYPES

if not isinstance(api_settings.AUTH_HEADER_TYPES, (list, tuple)):
    AUTH_HEADER_TYPES = (AUTH_HEADER_TYPES,)

AUTH_HEADER_TYPE_BYTES = set(
    h.encode(HTTP_HEADER_ENCODING)
    for h in AUTH_HEADER_TYPES
)


class CustomAuth:
    www_authenticate_realm = 'api'

    def authenticate(self, request):
        # auth = get_authorization_header(request).decode(HTTP_HEADER_ENCODING).split()
        auth_header = get_authorization_header(request).decode(HTTP_HEADER_ENCODING)
        auth = auth_header.split()
        """
        Returns two-tuple of (user, token) if authentication succeeds,
        or None otherwise.
        """
        if len(auth[1]) == 30:
            OAuth2Authentication.authenticate()

            def _dict_to_string(self, my_dict):
                """
                Return a string of comma-separated key-value pairs (e.g. k="v",k2="v2").
                """
                return ",".join([
                    '{k}="{v}"'.format(k=k, v=v)
                    for k, v in my_dict.items()
                ])

            def authenticate(self, request):
                oauthlib_core = get_oauthlib_core()
                valid, r = oauthlib_core.verify_request(request, scopes=[])
                print(valid)
                if valid:
                    return r.user, r.access_token
                request.oauth2_error = getattr(r, "oauth2_error", {})
                return None

            def authenticate_header(self, request):
                """
                Bearer is the only finalized type currently
                """
                www_authenticate_attributes = OrderedDict([
                    ("realm", self.www_authenticate_realm,),
                ])
                oauth2_error = getattr(request, "oauth2_error", {})
                www_authenticate_attributes.update(oauth2_error)
                return "Bearer {attributes}".format(
                    attributes=self._dict_to_string(www_authenticate_attributes),
                )
        else:

            www_authenticate_realm = 'api'

            def authenticate(self, request):
                header = self.get_header(request)
                if header is None:
                    return None

                raw_token = self.get_raw_token(header)
                if raw_token is None:
                    return None

                validated_token = self.get_validated_token(raw_token)

                return self.get_user(validated_token), validated_token

            def authenticate_header(self, request):
                return '{0} realm="{1}"'.format(
                    AUTH_HEADER_TYPES[0],
                    self.www_authenticate_realm,
                )

            def get_header(self, request):
                """
                Extracts the header containing the JSON web token from the given
                request.
                """
                header = request.META.get('HTTP_AUTHORIZATION')

                if isinstance(header, str):
                    # Work around django test client oddness
                    header = header.encode(HTTP_HEADER_ENCODING)

                return header

            def get_raw_token(self, header):
                """
                Extracts an unvalidated JSON web token from the given "Authorization"
                header value.
                """
                parts = header.split()

                if len(parts) == 0:
                    # Empty AUTHORIZATION header sent
                    return None

                if parts[0] not in AUTH_HEADER_TYPE_BYTES:
                    # Assume the header does not contain a JSON web token
                    return None

                if len(parts) != 2:
                    raise AuthenticationFailed(
                        _('Authorization header must contain two space-delimited values'),
                        code='bad_authorization_header',
                    )

                return parts[1]

            def get_validated_token(self, raw_token):
                """
                Validates an encoded JSON web token and returns a validated token
                wrapper object.
                """
                messages = []
                for AuthToken in api_settings.AUTH_TOKEN_CLASSES:
                    try:
                        return AuthToken(raw_token)
                    except TokenError as e:
                        messages.append({'token_class': AuthToken.__name__,
                                         'token_type': AuthToken.token_type,
                                         'message': e.args[0]})

                raise InvalidToken({
                    'detail': _('Given token not valid for any token type'),
                    'messages': messages,
                })

            def get_user(self, validated_token):
                """
                Attempts to find and return a user using the given validated token.
                """
                try:
                    user_id = validated_token[api_settings.USER_ID_CLAIM]
                except KeyError:
                    raise InvalidToken(_('Token contained no recognizable user identification'))

                try:
                    user = User.objects.get(**{api_settings.USER_ID_FIELD: user_id})
                except User.DoesNotExist:
                    raise AuthenticationFailed(_('User not found'), code='user_not_found')

                if not user.is_active:
                    raise AuthenticationFailed(_('User is inactive'), code='user_inactive')

                return user

    def authenticate_header(self, request):
        """
        Bearer is the only finalized type currently
        """

        return 'Bearer backend realm="%s"' % self.www_authenticate_realm
