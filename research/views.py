from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import *
from .models import *
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
# Create your views here.

#class CardResearchView(generics.ListAPIView):


class DefaultResearchView(APIView):
    parser_class = (FileUploadParser, )
    queryset = Research.objects.all()
    serializer_class = ResearchSerializer
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        research = Research.objects.order_by('-id').filter(status = 2)
        serializer = ResearchSerializer(research, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


    def post(self, request, format=None):
       serializer = ResearchSerializer(data=request.DATA, files=request.FILES)
       if serializer.is_valid():
           serializer.save()
           return Response(serializer.data, status=status.HTTP_201_CREATED)
       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResearchViewFromOldest(APIView):
    parser_class = (FileUploadParser, )
    queryset = Research.objects.all()
    serializer_class = ResearchSerializer
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        research = Research.objects.order_by('id').filter(status = 2)
        serializer = ResearchSerializer(research, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class ResearchViewFromCheapest(APIView):
    parser_class = (FileUploadParser, )
    queryset = Research.objects.all()
    serializer_class = ResearchSerializer
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        research = Research.objects.order_by('-old_price').filter(status = 2)
        serializer = ResearchSerializer(research, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class ResearchViewToCheapest(APIView):
    parser_class = (FileUploadParser, )
    queryset = Research.objects.all()
    serializer_class = ResearchSerializer
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        research = Research.objects.order_by('old_price').filter(status = 2)
        serializer = ResearchSerializer(research, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class ResearchDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (AllowAny,)

    queryset = Research.objects.all()
    serializer_class = ResearchSerializer

