from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('order-form/', OrderFormCreateView.as_view()),
    path('orders/', OrderCreateView.as_view()),


]
