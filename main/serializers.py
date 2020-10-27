from rest_framework import serializers
from .models import *

from research.serializers import CategoryCountSerializer


from post.models import Post
class MobAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobApp
        fields = ('description', "image", "url") 

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ( 'info', )

class ContactInfoSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer(many=True)
    class Meta:
        model = ContactInfo
        fields = ("contacts", )

class PostForMainPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("header", "description",)
class InfoForMainPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Info
        fields = ("header", "description")
        
        
class MainPageSerializer(serializers.ModelSerializer):
    mob_app = MobAppSerializer()
    сontacts = ContactInfoSerializer()
    category = CategoryCountSerializer(many=True)
    post = PostForMainPageSerializer()
    info = InfoForMainPageSerializer()

    class Meta:
        model = MainPage
        fields = ("info", "category", "post", "mob_app", "сontacts", )
        



