from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import *
from .models import *
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import AllowAny

# Create your views here.

class InfoView(generics.ListAPIView):
    parser_class = (FileUploadParser, )
    permission_classes = [AllowAny, ]
    serializer_class = InfoSerializer
    queryset = Info.objects.all()
      

  
class PostListView(generics.ListAPIView):
    parser_class = (FileUploadParser, )
    permission_classes = [AllowAny, ]
    serializer_class = PostSerializer
    queryset = Post.objects.all()
   
        
class NewsListView(generics.ListAPIView):
    parser_class = (FileUploadParser, )
    serializer_class = NewsSerializer
    queryset = News.objects.all().order_by('-id')
    permission_classes = [AllowAny, ]


    
class PostDetail(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny, ]
