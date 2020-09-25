from rest_framework import serializers
from .models import *

class InfoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Info
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = "__all__"

class NewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = News
        fields = "__all__"