from rest_framework import serializers
from .models import *
from django.utils.translation import ugettext_lazy as _


class CategorySerializer(serializers.ModelSerializer):
    count = serializers.IntegerField(source='get_recursive_product_count')

    class Meta:
        model = Category
        fields = ('id', 'name', 'parent', 'count')


class HashtagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hashtag
        fields = ('id', 'name')


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = ('id', 'name')


class CategoryCountSerializer(serializers.ModelSerializer): 
    count = serializers.IntegerField(source='get_recursive_product_count')
    
    class Meta:    
        model = Category 
        fields = ('id', 'name', 'count',)
class CategorySubCategory(serializers.ModelSerializer):
    subcategories = CategoryCountSerializer(source = 'get_categories', many = True)
    class Meta:
        model = Category
        fields = ('id', 'name', 'subcategories', )


class CardResearchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Research
        fields = ("id", "name", "image", "old_price", "pages")


class AboutMeSection(serializers.ModelSerializer):
    class Meta:
        model = QAdmins
        fields = ['about_me', 'logo', 'id']
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = QAdmins
        fields = ('logo', )


class ResearchSerializer(serializers.ModelSerializer):
    hashtag = HashtagSerializer(read_only=True, many=True)
    country = CountrySerializer(read_only=True, many=True)
    name_ = serializers.ReadOnlyField(source='get_name')
    description_ = serializers.ReadOnlyField(source='get_description')
    category = serializers.PrimaryKeyRelatedField(
            queryset=Category.objects.all()
        )
    author = AboutMeSection(read_only=True)

    def get_name(self):
        return _(self.name)

    def get_description(self):
        return _(self.name)
    
    similars = CardResearchSerializer(source = 'similar_researches', many = True, read_only=True)

    class Meta:
        model = Research
        fields = ('id', 'name_', 'name', 'description', 'image', 'date', 'pages', 'old_price', 'new_price', 'description_', 'hashtag', 'category', 'demo', 'country', 'status',
                  'similars', 'author', 'author')
        read_only_fields = ('date', 'status', 'hashtag', 'similars', 'category')

    def create(self, validated_data):
        research = Research.objects.create(author=self.context['request'].user.initial_reference, **validated_data)
        return research


class ResearchUpdateSerializer(serializers.ModelSerializer):
    name_ = serializers.ReadOnlyField(source='get_name')
    description_ = serializers.ReadOnlyField(source='get_description')

    def get_name(self):
        return _(self.name)

    def get_description(self):
        return _(self.name)

    class Meta:
        model = Research
        read_only_fields = [
            'name_', 'name', 'description', 'image', 'date', 'pages', 'old_price', 'new_price',
            'description_', 'hashtag', 'category', 'demo', 'country', 'status', 'research', 'similars', 'author',
            'date', 'status', 'hashtag', 'similars', 'category']

        fields = ['new_price', 'hashtag', 'country', 'description_', 'name_', 'category', 'similars']

