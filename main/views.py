from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import *
from .models import *
from rest_framework.permissions import AllowAny
from rest_framework.parsers import FileUploadParser


# Create your views here.
class MainPageView(generics.ListAPIView):
    permission_classes = [AllowAny, ]
    parser_class = (FileUploadParser, )
    queryset = MainPage.objects.all()
    serializer_class = MainPageSerializer
class SocialNetworksView(generics.ListAPIView):
    permission_classes = [AllowAny, ]
    parser_class = (FileUploadParser, )
    queryset = SocialNetworks.objects.all()
    serializer_class = SocialNetworksSerializer
