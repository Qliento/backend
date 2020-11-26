from rest_framework import serializers
from .models import *
from django.utils.translation import ugettext_lazy as _
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.exceptions import ObjectDoesNotExist
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
        fields = ("id", "name", "image", "old_price", "pages", 'demo', 'new_price',
                  'hashtag', 'date', 'country', 'author')


class ResearchFilePathSerializer(serializers.ModelSerializer):

    class Meta:
        model = ResearchFiles
        fields = ['id', 'name']


class ResearchSerializer(serializers.ModelSerializer):
    hashtag = HashtagSerializer(many=True, required=False)
    country = CountrySerializer(many=True, required=False)
    name_ = serializers.ReadOnlyField(source='get_name')
    description_ = serializers.ReadOnlyField(source='get_description')
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    author = AboutMeSection(read_only=True)
    research_data = ResearchFilePathSerializer(read_only=True, many=True)

    def get_name(self):
        return _(self.name)

    def get_description(self):
        return _(self.name)
    similars = CardResearchSerializer(source = 'similar_researches', many = True, read_only=True)

    class Meta:
        model = Research
        fields = ('id', 'name_', 'name', 'description', 'image', 'date', 'pages', 'old_price', 'new_price',
                  'description_', 'hashtag', 'category', 'demo', 'country', 'status',
                  'similars', 'author', 'content',
                  'research_data'
                  )
        read_only_fields = ('date', 'status', 'similars', 'new_price')

    def create(self, validated_data):
        files_of_research = self.context.get('request').FILES
        files_of_research.pop('demo')
        research = Research.objects.create(author=self.context['request'].user.initial_reference, **validated_data)
        all_hashtags = []
        all_countries = []

        for file in files_of_research.values():
            ext = os.path.splitext(file.name)[1]
            if not ext.lower() in ['.pdf', '.doc', '.docx', '.jpg', '.png', '.xlsx', '.xls', '.csv']:

                raise serializers.ValidationError("Неподдерживаемый тип данных")

            else:
                a = ResearchFiles.objects.create(research=research, name=file)

        hashtag_name = self.context.get('request').POST.__getitem__('hashtag')
        if not hashtag_name.isdigit():
            validated_data['hashtag'] = hashtag_name

            split_hashtags = hashtag_name.split()
            for i in split_hashtags:
                try:
                    created = Hashtag.objects.get(name=i.replace(',', ''))
                    get_id_if_yes = created.id
                    add_if_yes = research.hashtag.add(get_id_if_yes)
                    all_hashtags.append(add_if_yes)
                except ObjectDoesNotExist:
                    hashtag = research.hashtag.create(name=i.replace(',', ''))
                    all_hashtags.append(hashtag)

        else:
            raise serializers.ValidationError("Хэштеги не должны содержать числа")

        country_names = self.context.get('request').POST.__getitem__('country')
        if not country_names.isdigit():
            validated_data['country'] = country_names

            split_countries = country_names.split()
            for country in split_countries:
                try:
                    created = Country.objects.get(name=country.replace(',', ''))
                    add_id_if_country_exists = created.id
                    add_if_true = research.country.add(add_id_if_country_exists)
                    all_countries.append(add_if_true)
                except ObjectDoesNotExist:
                    state = research.country.get_or_create(name=country.replace(',', ''))
                    all_countries.append(state)

        else:
            raise serializers.ValidationError("Страны не должны содержать числа")

        return research


# class ResearchUpdateSerializer(serializers.ModelSerializer):
#     name_ = serializers.ReadOnlyField(source='get_name')
#     description_ = serializers.ReadOnlyField(source='get_description')
#
#     def get_name(self):
#         return _(self.name)
#
#     def get_description(self):
#         return _(self.name)
#
#     class Meta:
#         model = Research
#         read_only_fields = [
#             'name_', 'name', 'description', 'image', 'date', 'pages', 'old_price', 'new_price',
#             'description_', 'hashtag', 'category', 'demo', 'country', 'status', 'research_data', 'similars', 'author',
#             'date', 'status', 'hashtag', 'similars', 'category']
#
#         fields = ['new_price', 'hashtag', 'country', 'description_', 'name_', 'category', 'similars']


class DiscountPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Research
        fields = ['new_price']


class ResearchRetrieveSerializer(serializers.ModelSerializer):
    name_ = serializers.ReadOnlyField(source='get_name')
    description_ = serializers.ReadOnlyField(source='get_description')
    about_author = serializers.ReadOnlyField(source='author.about_me')

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

        fields = ['name_', 'name', 'description', 'image', 'date', 'pages', 'old_price', 'new_price',
            'description_', 'hashtag', 'category', 'demo', 'country', 'status', 'research_data', 'similars', 'author',
            'date', 'status', 'hashtag', 'similars', 'category', 'about_author']
