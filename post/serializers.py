from rest_framework import serializers
from .models import *

class ImagePostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ImagePost
        fields = "__all__"

class ImageInfoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ImageInfo
        fields = "__all__"

class InfoSerializer(serializers.ModelSerializer):
    images = ImageInfoSerializer(many = True)
    
    class Meta:
        model = Info
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):

    images = ImagePostSerializer(many = True)
    class Meta:
        model = Post
        fields = ('header', 'description', 'date', 'images')

class NewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = News
        fields = "__all__"
        
#TO-DO nested serializers for images