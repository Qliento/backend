import json
from rest_framework import status
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from .models import *
from .serializers import *

client = APIClient()


from django.test import RequestFactory, TestCase

from .views import *

class FAQTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.question = Question.objects.create(question = "Test?", answer = "Test.")

    def test_details(self):
        # Create an instance of a GET request.
        request = self.factory.get('/faq/')
        response = QuestionView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        

class PartnershipTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.partnership_info = PartnershipInfo.objects.create()
        self.partnership = Partnership.objects.create(header = 'Test', description = 'test', partnership = self.partnership_info)
    

    def test_details(self):
        # Create an instance of a GET request.
        request = self.factory.get('/partnership/')
        response = QuestionView.as_view()(request)
        self.assertEqual(response.status_code, 200)
