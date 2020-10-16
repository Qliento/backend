from rest_framework import serializers
from .models import *
from django.utils.translation import ugettext_lazy as _
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
    name_ = serializers.ReadOnlyField(source='get_name')
    description_ = serializers.ReadOnlyField(source='get_description')
    category = serializers.PrimaryKeyRelatedField(
            queryset = Category.objects.all()
        )

    def get_name(self):
        return _(self.name)

    def get_description(self):
        return _(self.name)
    
    similars = CardResearchSerializer(source = 'similar_researches', many = True, read_only=True)
    class Meta:
        model = Research
        fields = "__all__"
        read_only_fields = ('date', 'status', 'hashtag', 'similars', 'category')
    def create(self, validated_data):
        research = Research.objects.create(author=self.context['request'].user, **validated_data)
        return research
