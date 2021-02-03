from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid
from django.utils.html import mark_safe
from django.utils.translation import ugettext_lazy as _
import datetime
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **kwargs):
        if email is None:
            raise ValueError('Users must have email')

        user = self.model(
                          email=self.normalize_email(email),

                          **kwargs
                          )
        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **kwargs):
        if password is None:
            raise ValueError('Users must have password')

        user = self.create_user(email,
                                password=password,
                                )
        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)

        return user


class Users(AbstractBaseUser, PermissionsMixin):
    photo = models.ImageField(null=True, blank=True, upload_to='images', verbose_name='Изображение')
    name = models.CharField(max_length=120, default='ФИО', null=False, blank=False, verbose_name=" Имя")
    surname = models.CharField(max_length=120, default='ФИО', null=False, blank=False, verbose_name=" Фамилия")
    email = models.EmailField(max_length=120, unique=True, verbose_name="Электронная почта")
    phone_number = models.CharField(default='', verbose_name='Номер телефона', max_length=20)
    provider = models.CharField(default='email', max_length=20, blank=True, null=True, verbose_name='Способ регистрации')
    REQUIRED_FIELDS = ['password']
    USERNAME_FIELD = 'email'
    objects = UserManager()
    is_active = models.BooleanField(default=False, verbose_name="Активный пользователь")
    is_staff = models.BooleanField(default=False, verbose_name="Административные права")

    class Meta:
        verbose_name = _("Пользователь")
        verbose_name_plural = _('Все пользователи')

    def save(self, *args, **kwargs):
        users = Users.objects.filter(email__iexact=self.email).count()
        if users == 1 or users == 0:
            super(Users, self).save(*args, **kwargs)

    def tokens(self):
        token_refresh = RefreshToken.for_user(self)
        creds = {"refresh": str(token_refresh),
                 "access": str(token_refresh.access_token)}
        return creds


class Clients(models.Model):
    client_status = models.OneToOneField(Users, on_delete=models.CASCADE, related_name="primary_reference")

    class Meta:
        verbose_name = _("Заказчик")
        verbose_name_plural = _('Заказчики')

    def __str__(self):
        return self.client_status.name


class QAdmins(models.Model):
    admin_status = models.OneToOneField(Users, on_delete=models.CASCADE, related_name="initial_reference")
    logo = models.CharField(verbose_name="Название организации", max_length=100)
    about_me = models.TextField(max_length=2000)
    position = models.CharField(blank=True, null=True, verbose_name="Должность", max_length=100)

    class Meta:
        verbose_name = _("Партнёр")
        verbose_name_plural = _('Партнёры')

    def __str__(self):
        return self.admin_status.email


class UsersConsentQliento(models.Model):
    text = models.TextField(max_length=2000)

    class Meta:
        verbose_name = _("Пользовательское соглашение")
        verbose_name_plural = _('Пользовательское соглашение')
