import json
from rest_framework import status
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from .models import *
from post.models import *
from research.models import *
from .serializers import *

client = APIClient()


from django.test import RequestFactory, TestCase

from .views import *

class MainPageTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.contact_info = ContactInfo.objects.create()
        self.contacts = Contact.objects.create(info = "Test", contactInfo = self.contact_info)
        self.info = Info.objects.create(header = 'Test', description = 'test')
        self.post = Post.objects.create(header = 'Test', description = 'test')
        self.category = Category.objects.create(name = "Test category") 
        self.mob_app = MobApp.objects.create(header = 'Test', description = 'test', url = 'www.test.com')
        self.main_page = MainPage.objects.create(info = self.info,  post = self.post, mob_app = self.mob_app, сontacts = self.contact_info)
        self.main_page.category.add(1)

    def test_details(self):
        # Create an instance of a GET request.
        request = self.factory.get('/main-page/')
        response = MainPageView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        

class SNTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.sn = SocialNetworks.objects.create(name = 'Test', url = 'www.test.com')

    def test_details(self):
        # Create an instance of a GET request.
        request = self.factory.get('/social-networks/')
        response = SocialNetworksView.as_view()(request)
        self.assertEqual(response.status_code, 200)

