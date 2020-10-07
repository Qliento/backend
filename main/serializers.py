from rest_framework import serializers
from .models import *
from post.serializers import *
from research.serializers import *


class MobAppSerializer(serializers.ModelSerializer):
	class Meta:
		model = MobApp
		fields = "__all__" 
class ContactInfoSerializer(serializers.ModelSerializer):
	class Meta:
		model = ContactInfo
		fields = ("number", "email")

class MainPageSerializer(serializers.ModelSerializer):
    categories = CategoryCountSerializer(many = True)
    news = NewsSerializer(many = True)
    about_us = InfoSerializer()
    analytic = PostSerializer()
    mob_app = MobAppSerializer()
    сontacts = ContactInfoSerializer()

    class Meta:
        model = MainPage
        fields = "__all__"
        



