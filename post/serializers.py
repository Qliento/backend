from rest_framework import serializers
from .models import *
from research.serializers import CardResearchSerializer

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
        fields = ('id', 'header', 'description', 'images')



class PostSerializer(serializers.ModelSerializer):

    images = ImagePostSerializer(many = True)
    research = CardResearchSerializer()
    class Meta:
        model = Post
        fields = ('header', 'description', 'date', 'images', 'research')

class NewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = News
        fields = ('id', 'name', 'description', 'date', 'source')
        
