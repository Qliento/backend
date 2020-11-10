from django.urls import path

from .views import *

app_name = 'main'
urlpatterns = [
    path('main-page/', MainPageView.as_view()),
    path('social-networks/', SocialNetworksView.as_view()),
]
