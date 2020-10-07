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
class QuestionView(generics.ListAPIView):
	queryset = Question.objects.all()
	serializer_class = QuestionSerializer

class PartnershipView(generics.ListAPIView):
	queryset = Partnership.objects.all()
	serializer_class = PartnershipSerializer

class FeedbackView(APIView):
	def post(self, request, format=None):
			serializer = SnippetSerializer(data=request.data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status=status.HTTP_201_CREATED)
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)