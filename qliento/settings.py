"""
Django settings for qliento project.

Generated by 'django-admin startproject' using Django 3.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
from django.utils.translation import gettext_lazy as _
from datetime import timedelta

# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ay@g8$$0c!$+c9h1xt^f6sk5!12zp^pmnc1%xmj8_2fh$#_$42'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'modeltranslation',
    'jet.dashboard',
    'jet',

    'corsheaders',
    'post.apps.PostConfig',
    'research.apps.ResearchConfig',
    'main.apps.MainConfig',
    'question.apps.QuestionConfig',

    'rest_framework',
    'django_simple_tags',
    'django_horizontal_list_filter',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'mptt',
    'django_filters',
    'jwt',
    'djoser',

    'oauth2_provider',
    'social_django',
    'rest_framework_social_oauth2',

    'rest_framework_simplejwt',
    'rest_framework.authtoken',


    # 'django_hosts',
    'rest_framework_recaptcha',
    'registration',
    'orders',

]


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',   
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'qliento.utils.ActivateTranslationMiddleware',
    'qliento.utils.AdminLocaleURLMiddleware',
    'qliento.utils.corsMiddleware',
    

]

ROOT_URLCONF = 'qliento.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates/')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                
            ],
        },
    },
]
JET_SIDE_MENU_COMPACT = True
WSGI_APPLICATION = 'qliento.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'qliento',
            'USER': 'postgres',
            'PASSWORD': '3WYe^n;s5>GA',
            'HOST': 'localhost',
            'PORT': ''
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'qliento',
            'USER': 'admin',
            'PASSWORD': '78sf45sf47asf@',
            'HOST': 'localhost',
            'PORT': ''
        }
    }

AUTH_USER_MODEL = 'registration.Users'
# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

REST_FRAMEWORK =  {
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'registration.backends.TokenAuthentication',
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'rest_framework_social_oauth2.authentication.SocialAuthentication',
    ],

    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
        'rest_framework.permissions.IsAuthenticated',
    ],
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
    )
}

SIMPLE_JWT = {
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1000),
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=1440)
}

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/
ADMIN_LANGUAGE_CODE= 'ru'
LANGUAGE_CODE = 'ru-ru'

from django.conf import global_settings

gettext = lambda s: s
LANGUAGES = (
    ('ru', 'Russian'),
    ('ky', gettext('Kyrgyz')),
    ('en', gettext('English')),
)

EXTRA_LANG_INFO = {
    'ky': {
        'bidi': False,
        'code': 'ky',
        'name': 'Kyrgyz',
        'name_local': 'Кыргызча',
    },
}


import django.conf.locale
LANG_INFO = dict(django.conf.locale.LANG_INFO, **EXTRA_LANG_INFO)
django.conf.locale.LANG_INFO = LANG_INFO

LANGUAGES_BIDI = global_settings.LANGUAGES_BIDI + ["ky"]

USE_I18N = True
USE_L10N = True

TIME_ZONE = 'UTC'


USE_TZ = True
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)



STATIC_URL = '/static/'
MEDIA_URL = '/files/'

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')

STATTIC_DIRS = [ os.path.join(BASE_DIR, 'static') ]

MEDIA_ROOT = os.path.join(BASE_DIR, 'static/files')
PREFIX_DEFAULT_LOCALE = ''

EMAIL_HOST = 'smtp.sendgrid.net'
DEFAULT_FROM_EMAIL = 'qlientoinfo@gmail.com'
EMAIL_HOST_USER = 'qlientoinfo@gmail.com'
EMAIL_HOST_PASSWORD = 'ofniotneilq1'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# reCAPTCHA settings
DRF_RECAPTCHA_SECRET_KEY = '6LcrLtEZAAAAACZHldmSPfvgnUHbuc5KvvHJrA3z'

# client_id = 6LcrLtEZAAAAAPc2hmaPPXHT_xqscPUIgey_M8n6

AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.vk.VKOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_PIPELINE = (
  'social_core.pipeline.social_auth.social_details',
  'social_core.pipeline.social_auth.social_uid',
  'social_core.pipeline.social_auth.auth_allowed',
  'social_core.pipeline.social_auth.social_user',
  'social_core.pipeline.user.get_username',
  'social_core.pipeline.social_auth.associate_by_email',
  'social_core.pipeline.user.create_user',
  'social_core.pipeline.social_auth.associate_user',
  'social_core.pipeline.social_auth.load_extra_data',
  'social_core.pipeline.user.user_details',
)

# Facebook configuration
SOCIAL_AUTH_FACEBOOK_KEY = '270558847271418'
SOCIAL_AUTH_FACEBOOK_SECRET = 'b4d9759f8ddd09f6e76eec20d94dba3d'

# Define SOCIAL_AUTH_FACEBOOK_SCOPE to get extra permissions from Facebook.
# Email is not sent by default, to get it, you must request the email permission.
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', 'name', 'password']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'id, name, email, password'
}
# VK configuration
SOCIAL_AUTH_VK_OAUTH2_KEY = '7609809'
SOCIAL_AUTH_VK_OAUTH2_SECRET = '4aIt5YSoctAFqeX9g15V'
SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['email']
# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators


# Google configuration

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '1032556798687-6427pbbpse1jm5ho5is64cja01bad94u.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'tNKrBMOuSdxkoQTOknLeTyLm'
# LOGIN_URL = '/auth/login/google-oauth2/'
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
]
# LOGIN_REDIRECT_URL = '/'
# LOGOUT_REDIRECT_URL = '/'

# HTTPS configuration
SOCIAL_AUTH_REDIRECT_IS_HTTPS = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = False
