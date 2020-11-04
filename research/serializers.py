from rest_framework import serializers
from .models import *
from django.utils.translation import ugettext_lazy as _


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
    research_data = ResearchFilePathSerializer(many=True)

    def get_name(self):
        return _(self.name)

    def get_description(self):
        return _(self.name)
    
    similars = CardResearchSerializer(source = 'similar_researches', many = True, read_only=True)

    class Meta:
        model = Research
        fields = ('id', 'name_', 'name', 'description', 'image', 'date', 'pages', 'old_price', 'new_price', 'description_', 'hashtag', 'category', 'demo', 'country', 'status','research_data',
                  'similars', 'author', 'author', 'content', )
        read_only_fields = ('date', 'status', 'hashtag', 'similars', 'category')

    def create(self, validated_data):
        research = Research.objects.create(author=self.context['request'].user.initial_reference, **validated_data)

        files_of_research = validated_data.pop('research_data')
        for file_of_research in files_of_research:
            ResearchFiles.objects.create(research=research, **file_of_research)

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

