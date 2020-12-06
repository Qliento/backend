from django.contrib import admin
from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView
# from .social_logins import SocialLoginView


urlpatterns = [
    path('registration/researchers/', QAdminRegistration.as_view()),
    path('email-verification/', VerifyEmail.as_view(), name='email-verify'),
    path('registration/clients/', ClientsRegistration.as_view()),

    path('login/clients/', login_respondents),

    path('update/users/', UsersUpdate.as_view()),
    path('update/partners/', PartnersUpdate.as_view()),

    path('send-email/', send_email),
    path('password-update/', PasswordReset.as_view()),

    path('my-researches/', MyUploadedResearches.as_view()),
    path('download-file/<int:pk>/', DownloadFileView.as_view()),
    path('qliento-consent/', UserConsentView.as_view()),
    path('jwt-create/', UpdatedTokenObtainPairView.as_view()),
    path('jwt-refresh/', TokenRefreshView.as_view()),
    # path('login/facebook/', SocialLoginView.as_view())
    path('google/', GoogleSocialAuthView.as_view()),

]
