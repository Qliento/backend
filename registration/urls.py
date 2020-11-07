from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('registration/researchers/', QAdminRegistration.as_view()),
    path('email-verification/', VerifyEmail.as_view(), name='email-verify'),
    path('registration/clients/', ClientsRegistration.as_view()),

    path('login/researchers/', login_qadmins),
    path('login/clients/', login_respondents),

    path('update/users/', UsersUpdate.as_view()),
    path('update/partners/', PartnersUpdate.as_view()),

    path('send-email/', send_email),
    path('password-update/', PasswordReset.as_view()),

    path('my-researches/', MyUploadedResearches.as_view()),
    path('download-file/<int:pk>/', DownloadFileView.as_view())

]
