from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import *
from .models import *
from rest_framework.parsers import FileUploadParser

# Create your views here.

class InfoView(APIView):
    parser_class = (FileUploadParser, )
    queryset = Info.objects.all()
    
    def get(self, request, format=None):
        info = Info.objects.all()
        serializer = InfoSerializer(info, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)   

  
class PostListView(APIView):
    parser_class = (FileUploadParser, )
    queryset = Post.objects.all()

    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)   
        
class NewsListView(APIView):
    parser_class = (FileUploadParser, )
    queryset = News.objects.all()

    def get(self, request, format=None):
        news = News.objects.all()
        serializer = NewsSerializer(news, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK) 

class NewsDetail(generics.RetrieveAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
class PostDetail(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer