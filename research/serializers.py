from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = "__all__"


class HashtagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hashtag
        fields = "__all__"

class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = "__all__"

class ResearchSerializer(serializers.ModelSerializer):
    hashtag = HashtagSerializer(read_only=True, many=True)
    country = CountrySerializer(read_only=True, many=True)
    category = serializers.CharField(source = 'category.name')
    class Meta:
        model = Research
        fields = "__all__"
        read_only_fields = ('date', 'status', 'hashtag', )
        
