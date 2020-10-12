from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import *
from .models import *
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from rest_framework.permissions import AllowAny
# Create your views here.

#class CardResearchView(generics.ListAPIView):


class DefaultResearchView(APIView):
    permission_classes = [AllowAny, ]
    parser_classes = [MultiPartParser, FormParser]
    queryset = Research.objects.all()
    serializer_class = ResearchSerializer
    
    def get(self, request, format=None):
        research = Research.objects.order_by('-id').filter(status = 2)
        serializer = ResearchSerializer(research, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


    def post(self, request, *args, **kwargs):
        file_serializer = ResearchSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResearchViewFromOldest(APIView):
    permission_classes = [AllowAny, ]
    queryset = Research.objects.all()
    serializer_class = ResearchSerializer

    def get(self, request, format=None):
        research = Research.objects.order_by('id').filter(status = 2)
        serializer = ResearchSerializer(research, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class ResearchViewFromCheapest(APIView):
    permission_classes = [AllowAny, ]
    queryset = Research.objects.all()
    serializer_class = ResearchSerializer

    def get(self, request, format=None):
        research = Research.objects.order_by('-old_price').filter(status = 2)
        serializer = ResearchSerializer(research, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class ResearchViewToCheapest(APIView):
    permission_classes = [AllowAny, ]

    queryset = Research.objects.all()
    serializer_class = ResearchSerializer

    def get(self, request, format=None):
        research = Research.objects.order_by('old_price').filter(status = 2)
        serializer = ResearchSerializer(research, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
class ResearchDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny, ]
    queryset = Research.objects.all()
    serializer_class = ResearchSerializer
