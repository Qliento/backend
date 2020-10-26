from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import *
from .models import *
from registration.utils import Util
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from collections import OrderedDict
from rest_framework.permissions import AllowAny, IsAuthenticated
# Create your views here.

#class CardResearchView(generics.ListAPIView):


class DefaultResearchView(APIView):
    permission_classes = [AllowAny, ]
    parser_classes = [MultiPartParser, FormParser]
    queryset = Research.objects.all()
    serializer_class = ResearchSerializer
    
    def get(self, request, format=None):
        research = Research.objects.order_by('-id').filter(status=2)
        serializer = ResearchSerializer(research, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UploadResearchView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = Research.objects.all()
    serializer_class = ResearchSerializer

    def post(self, request, *args, **kwargs):
        file_serializer = self.get_serializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            get_name_of_research = list(request.data.values())[0]
            email_body = 'Доброго времени суток, Qliento! \n' + \
                         'Партнер: {}, отправил вам запрос на одобрение своего исследования. \n' \
                         'Название исследования: "{}". \n' \
                         'Пройдите пожалуйста в админ-панель для принятия дальнейших действий.'.format(request.user.name, get_name_of_research)

            data = {'email_body': email_body, 'to_email': 'qlientoinfo@gmail.com',
                    'email_subject': 'Исследование на подтверждение'}
            Util.send_email(data)

            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateResearchView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = Research.objects.all()
    serializer_class = ResearchUpdateSerializer

    def get(self, request, *args, **kwargs):
        self.queryset = Research.objects.filter(id=self.kwargs['pk'], author=request.user.initial_reference)
        return Response(data=list(self.queryset.values()), status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        try:
            my_queryset = Research.objects.filter(id=self.kwargs['pk'], author=request.user.initial_reference).update(new_price=request.data.get('new_price'))
            get_updated = Research.objects.filter(id=self.kwargs['pk'], author=request.user.initial_reference)
            return Response(list(get_updated.values())[0], status=status.HTTP_202_ACCEPTED)
        except ValueError:
            content = {'message': 'Убедитесь в том, что вы ввели целые числа'}
            return Response(content, status=status.HTTP_304_NOT_MODIFIED)


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
