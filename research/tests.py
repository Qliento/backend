import json
from rest_framework import status
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from .models import *
from .serializers import *
from registration.models import *
from rest_framework.authtoken.models import Token
from rest_framework.test import force_authenticate

client = APIClient()


from django.test import RequestFactory, TestCase

from .views import *

class SimpleTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.hashtag = Hashtag.objects.create(name = "Test hashtag")
        self.category = Category.objects.create(name = "Test category")
        self.subcategory = Category.objects.create(name = "Test subcategory", parent = self.category)
        self.status1 = Status.objects.create(name = "Test status1")
        self.status2 = Status.objects.create(name = "Test status2")
        self.country = Country.objects.create(name = "Test country")
        self.research = Research.objects.create(name = "Test research", category = self.subcategory, pages = 5, old_price = 10, new_price = 9, description = "Test description", content = "Test content", status = self.status2)
    
    def test_details(self):
        # Create an instance of a GET request.
        request = self.factory.get('/research/')
        response = DefaultResearchView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        

    def test_create_invalid_research(self):
        self.invalid_data = {
            "name": "Swedish",
            "description": "sometext",            
            "pages": 200,
            "old_price": 50,
            "new_price": 20,
            "hashtag": [],
            "demo": "http://127.0.0.1:8000/files/demos/Wet-street-water-dry-leaf-city_1920x1080_pMU73zX.jpg",
            "country": [],
            "status": "1",
            "category": 1,
            "research": "Повестка_дня_первая_презентация_соц_проектов.pdf"
}
        self.user = Users.objects.create_user(name='user@foo.com', email='user@foo.com', password='top_secret')
        self.token = Token.objects.create(user=self.user)
        self.token.save()
        request = self.factory.post('/research-upload/',self.invalid_data, content_type='application/json')
        force_authenticate(request, user=self.user, token=self.user.auth_token)
        response = UploadResearchView.as_view()(request)
        self.assertEqual(response.status_code, 400)
        