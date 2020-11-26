from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_404_NOT_FOUND
from .serializers import QAdminSerializer, UpdatePassword, ClientSerializer, \
    EmailVerificationSerializer, UsersUpdateSerializer, CleanedResearchSerializer, \
    CleanedFileOnly, UserConsentSerializer, CleanedDemoOnly, AdditionalInfoToken, QAdminUpdateSerializer
from .models import QAdmins, Users, Clients, UsersConsentQliento
from research.models import Research
from orders.models import Orders
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView, GenericAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
import secrets
import json
import string
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util
import jwt
from django.core.mail import send_mail
from django.http import FileResponse
from django.http import HttpResponseRedirect
from rest_framework import generics, permissions, status, views
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.renderers import JSONRenderer
from rest_framework_simplejwt.views import TokenObtainPairView
from requests.exceptions import HTTPError
from social_django.utils import load_strategy, load_backend, psa
from social_core.backends.oauth import BaseOAuth2
from social_core.exceptions import MissingBackend, AuthTokenError, AuthForbidden
# Create your views here.


class UpdatedTokenObtainPairView(TokenObtainPairView):
    serializer_class = AdditionalInfoToken


class QAdminRegistration(GenericAPIView):
    queryset = QAdmins.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = QAdminSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        admin_as_user = Users.objects.get(email=user_data['admin_status']['email'])
        token = RefreshToken.for_user(admin_as_user).access_token
        current_site = get_current_site(request).domain

        relative_link = reverse('email-verify')
        abs_url = 'http://' + current_site + relative_link + "?token=" + str(token)
        email_body = 'Добрый день, пользователь.' + ' Пройдите по этой ссылке ниже в течение 24 часов, чтобы войти на сайт. Ваша ссылка для активации: \n' + abs_url

        data = {'email_body': email_body, 'to_email': str(admin_as_user), 'email_subject': 'Verify your email'}
        Util.send_email(data)

        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer
    permission_classes = (AllowAny,)

    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = Users.objects.get(id=payload['user_id'])
            if not user.is_active:
                user.is_active = True
                user.save()
            return HttpResponseRedirect(redirect_to="http://qliento-project.surge.sh")
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class ClientsRegistration(GenericAPIView):
    queryset = Clients.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ClientSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        client_as_user = Users.objects.get(email=user_data['client_status']['email'])
        token = RefreshToken.for_user(client_as_user).access_token
        current_site = get_current_site(request).domain
        relative_link = reverse('email-verify')
        abs_url = 'http://' + current_site + relative_link + "?token=" + str(token)

        send_mail('Активация аккаунта',
                  'Доброго времени суток, пользователь. Пройдите по этой ссылке ниже в течение 24 часов, чтобы войти на сайт. Ваша ссылка для активации: %s' % abs_url,
                  settings.EMAIL_HOST_USER,
                  [str(client_as_user)],
                  fail_silently=False)

        return Response(user_data, status=status.HTTP_201_CREATED)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login_respondents(request):

    email = request.data.get("email")
    password = request.data.get("password")
    client_as_user = Users.objects.get(email=email)
    if client_as_user.is_active:
        if email is None or password is None:
            return Response({'error': 'Убедитесь в правильности вводимых данных'},
                            status=HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=email, password=password)

        if not user:
            return Response({'error': 'Убедитесь в правильности вводимых данных'},
                            status=HTTP_404_NOT_FOUND)
        token, created = Token.objects.get_or_create(user=user)

        content = {'message': 'Добро пожаловать'}
        return Response(content, status=200)
    else:
        return Response({'error': 'Вы не активировали ещё свой аккаунт. Пройдите по ссылке, которая была отправлена на вашу почту.'},
                        status=HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login_qadmins(request):

    email = request.data.get("email")
    password = request.data.get("password")
    qadmin_as_user = Users.objects.get(email=email)
    if qadmin_as_user.is_active:
        if email is None or password is None:
            return Response({'error': 'Введите почту и пароль'},
                            status=HTTP_400_BAD_REQUEST)
        user = authenticate(request, username=email, password=password)

        if not user:

            return Response({'error': 'Убедитесь в правильности вводимых данных'},
                            status=HTTP_404_NOT_FOUND)
        token, created = Token.objects.get_or_create(user=user)

        content = {'message': 'Добро пожаловать'}
        return Response(content, status=200)
    else:
        return Response({'error': ' Вы не активировали ещё свой аккаунт. Пройдите по ссылке, которая была отправлена на вашу почту.'},
                        status=HTTP_400_BAD_REQUEST)


class UsersUpdate(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UsersUpdateSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class PartnersUpdate(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = QAdminUpdateSerializer
    parser_classes = [JSONParser, MultiPartParser]

    def get(self, *args, **kwargs):
        serializer = self.serializer_class(QAdmins.objects.get(admin_status=self.request.user))
        return Response(serializer.data)

    def get_queryset(self):
        return QAdmins.objects.filter(admin_status=self.request.user)

    def perform_update(self, request, *args, **kwargs):
        serializer = QAdminUpdateSerializer(QAdmins.objects.get(admin_status=self.request.user), data=request.data, context=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        return self.perform_update(request, *args, **kwargs)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def send_email(request):
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(20))

    if request.method == "POST":
        try:
            value = request.data.get("email")

            users_email = Users.objects.filter(email=value)

            old_password = users_email.get()
            old_password.password = password

            old_password.set_password(password)
            old_password.save()

            send_mail('Временный пароль',
                      'Доброго времени суток, пользователь. '
                      'Используйте этот пароль ниже, чтобы войти на сайт и поменять на новый. '
                      'Ваш временный пароль: %s' % password,

                      settings.EMAIL_HOST_USER,
                      [value],
                      fail_silently=False)

            if old_password:
                content = {'message': 'Инструкция была отправлена на почту'}
                return Response(content, status=200)

        except Users.DoesNotExist:
            content = {'message': 'Напишите вашу почту корректно'}
            return Response(content, status=400)


class PasswordReset(UpdateAPIView):
    serializer_class = UpdatePassword
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # if using custom token, create a new token, because previous one was changed
        if hasattr(user, 'auth_token'):
            user.auth_token.delete()
        token, created = Token.objects.get_or_create(user=user)
        content = {'Ваш пароль был изменен'}
        return Response(content, status=status.HTTP_200_OK)


class MyUploadedResearches(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CleanedResearchSerializer
    queryset = None

    def get(self, request, *args, **kwargs):
        self.queryset = Research.objects.filter(author__admin_status=request.user)
        return self.list(request, *args, **kwargs)


class DownloadFileView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CleanedFileOnly
    parser_classes = [MultiPartParser, JSONParser]
    queryset = None

    def get(self, request, *args, **kwargs):
        try:
            self.queryset = Research.objects.filter(id=self.kwargs['pk'], ordered_items__buyer=request.user, ordered_items__items_to_pay__completed=True)
            file_itself = self.queryset.values('research')
            path_of_file = list(file_itself)[0].get('research')
            return FileResponse(open('static/files/{}'.format(path_of_file), 'rb'))

        except IndexError:
            content = {'message': 'Данное исследование не имеет файлов'}
            return Response(content, status=400)


class DownloadDemoView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CleanedDemoOnly
    parser_classes = [MultiPartParser, JSONParser]
    queryset = None

    def get(self, request, *args, **kwargs):
        try:
            self.queryset = Research.objects.filter(id=self.kwargs['pk'], status=2)
            file_itself = self.queryset.values('demo')
            path_of_file = list(file_itself)[0].get('demo')
            return FileResponse(open('static/files/{}'.format(path_of_file), 'rb'))

        except IndexError:
            content = {'message': 'Данное исследование не имеет файлов'}
            return Response(content, status=400)


class UserConsentView(generics.ListAPIView):
    permission_classes = [AllowAny, ]
    queryset = UsersConsentQliento.objects.all()
    serializer_class = UserConsentSerializer
