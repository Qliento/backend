from rest_framework import serializers
from .models import *
from django.utils.translation import ugettext_lazy as _
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.exceptions import ValidationError
import os


class CategorySerializer(serializers.ModelSerializer):
    parent = serializers.CharField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'parent',)


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

    subcategories = CategoryCountSerializer(source = 'get_subcategories', many = True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'subcategories', )


class AboutMeSection(serializers.ModelSerializer):
    class Meta:
        model = QAdmins
        fields = ['about_me', 'logo', 'id']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = QAdmins
        fields = ('logo', )


class CardResearchSerializer(serializers.ModelSerializer):
    hashtag = HashtagSerializer(read_only=True, many=True)
    country = CountrySerializer(read_only=True, many=True)
    author = AuthorSerializer()

    class Meta:
        model = Research
        fields = ("id", "name", "image", "old_price", "pages", 'demo', 'new_price', 'hashtag', 'date', 'country', 'author')


class ResearchFilePathSerializer(serializers.ModelSerializer):

    class Meta:
        model = ResearchFiles
        fields = ['id', 'name']


class ResearchSerializer(serializers.ModelSerializer):
    hashtag = HashtagSerializer(read_only=True, many=True)
    country = CountrySerializer(read_only=True, many=True)
    name_ = serializers.ReadOnlyField(source='get_name')
    description_ = serializers.ReadOnlyField(source='get_description')
    category = CategorySerializer()
    author = AboutMeSection(read_only=True)
    research_data = ResearchFilePathSerializer(read_only=True, many=True)

    def get_name(self):
        return _(self.name)

    def get_description(self):
        return _(self.name)
    
    similars = CardResearchSerializer(source = 'similar_researches', many = True, read_only=True)

    class Meta:
        model = Research
        fields = ('id', 'name_', 'name', 'description', 'image', 'date', 'pages', 'old_price', 'new_price', 'description_', 'hashtag', 'category', 'demo', 'country', 'status',
                  'similars', 'author', 'author', 'content',
                  'research_data'
                  )
        read_only_fields = ('date', 'status', 'hashtag', 'similars', 'category')

    def create(self, validated_data):

        files_of_research = self.context.get('request').FILES
        files_of_research.pop('demo')

        research = Research.objects.create(author=self.context['request'].user.initial_reference, **validated_data)

        for file in files_of_research.values():
            ext = os.path.splitext(file.name)[1]
            if not ext.lower() in ['.pdf', '.doc', '.docx', '.jpg', '.png', '.xlsx', '.xls', '.csv']:

                raise serializers.ValidationError("Неподдерживаемый тип данных")

            else:
                a = ResearchFiles.objects.create(research=research, name=file)

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
            'description_', 'hashtag', 'category', 'demo', 'country', 'status', 'research_data', 'similars', 'author',
            'date', 'status', 'hashtag', 'similars', 'category']

        fields = ['new_price', 'hashtag', 'country', 'description_', 'name_', 'category', 'similars']

