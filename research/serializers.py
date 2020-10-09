from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = "__all__"
class CategoryCountSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField(source='get_recursive_product_count')

    class Meta:
        model = Category
        fields = ('name', 'count',)

class HashtagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hashtag
        fields = "__all__"

class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = "__all__"

class CardResearchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Research
        fields = ("id", "name", "image", "old_price", "pages")


class ResearchSerializer(serializers.ModelSerializer):
    hashtag = HashtagSerializer(read_only=True, many=True)
    country = CountrySerializer(read_only=True, many=True)
    category = serializers.CharField(source = 'category.name')
    similars = CardResearchSerializer(source = 'similar_researches', many = True)
    author = serializers.PrimaryKeyRelatedField(read_only=True, source='author.name')

    class Meta:
        model = Research
        fields = "__all__"
        read_only_fields = ('date', 'status', 'hashtag', 'similars')

    def create(self, validated_data):
        research = Research.objects.create(author=self.context['request'].user, **validated_data)
        return research
