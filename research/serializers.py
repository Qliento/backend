from rest_framework import serializers
from .models import *
from django.utils.translation import ugettext_lazy as _
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.exceptions import ObjectDoesNotExist
import os
import json
from orders.models import Statistics
import secrets
import string

from collections import OrderedDict


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
        fields = ('logo', 'about_me')


class ContentDataInfo(serializers.ModelSerializer):

    class Meta:
        model = ResearchContent
        fields = ['content', 'page']


class SimilarResearchSerializer(serializers.ModelSerializer):
    hashtag = HashtagSerializer(read_only=True, many=True)
    country = CountrySerializer(read_only=True, many=True)
    author = AuthorSerializer()

    class Meta:
        model = Research
        fields = ("id", "name", "image", "old_price", "pages", 'new_price', 'demo',
                  'hashtag', 'date', 'country', 'author')

    def to_representation(self, instance):
        data = super(SimilarResearchSerializer, self).to_representation(instance)
        data.pop('image')
        data.pop('demo')
        data['image'] = instance.clean_image_path
        data['demo'] = instance.clean_demo_path
        return data


class CardResearchSerializer(serializers.ModelSerializer):
    hashtag = HashtagSerializer(read_only=True, many=True)
    country = CountrySerializer(read_only=True, many=True)
    author = AuthorSerializer()
    content_data = ContentDataInfo(read_only=True, many=True)
    similars = SimilarResearchSerializer(source = 'similar_researches', many=True, read_only=True)

    class Meta:
        model = Research
        fields = ("id", "name", "image", "old_price", "pages", 'new_price', 'demo',
                  'hashtag', 'date', 'country', 'author', 'content_data', 'description', 'similars')

    def to_representation(self, instance):
        data = super(CardResearchSerializer, self).to_representation(instance)
        data.pop('image')
        data.pop('demo')

        data['image'] = instance.clean_image_path
        data['demo'] = instance.clean_demo_path
        try:
            data.pop('content_data')
            header = self.context.get('request').headers.get('Accept-Language')
            empty_content_data = []
            contents = ResearchContent.objects.filter(content_data=instance.id)

            s = None

            for i in contents:

                the_value = getattr(i, 'content'+'_{}'.format(header))

                if the_value is None:
                    continue
                elif the_value is not None:
                    s = the_value
                    empty_content_data.append({'content': getattr(i, 'content' + '_{}'.format(header)),
                                               'page': getattr(i, 'page' + '_{}'.format(header))})

            if s is None:
                data['content_data'] = []

            elif s is not None:
                data['content_data'] = empty_content_data

            else:
                data['content_data'] = 'Error'

            return data

        except AttributeError:
            return data


class AdminCardResearchSerializer(serializers.ModelSerializer):
    hashtag = HashtagSerializer(read_only=True, many=True)
    country = CountrySerializer(read_only=True, many=True)
    author = AuthorSerializer()
    content_data = ContentDataInfo(read_only=True, many=True)

    class Meta:
        model = Research
        fields = ("id", "name", "image", "old_price", "pages", 'new_price', 'demo', 'status',
                  'hashtag', 'date', 'country', 'author', 'content_data', 'description')

    def to_representation(self, instance):
        data = super(AdminCardResearchSerializer, self).to_representation(instance)

        try:
            data.pop('content_data')
            header = self.context.get('request').headers.get('Accept-Language')
            empty_content_data = []
            contents = ResearchContent.objects.filter(content_data=instance.id)

            s = None

            for i in contents:

                the_value = getattr(i, 'content' + '_{}'.format(header))

                if the_value is None:
                    continue
                elif the_value is not None:
                    s = the_value
                    empty_content_data.append({'content': getattr(i, 'content' + '_{}'.format(header)),
                                               'page': getattr(i, 'page' + '_{}'.format(header))})

            if s is None:
                data['content_data'] = []

            elif s is not None:
                data['content_data'] = empty_content_data

            else:
                data['content_data'] = 'Error'

        except AttributeError:
            return data


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
    similars = CardResearchSerializer(source = 'similar_researches', many = True, read_only=True)
    content_data = ContentDataInfo(many=True)

    def get_name(self):
        return _(self.name)

    def get_description(self):
        return _(self.name)

    class Meta:
        model = Research
        fields = ('id', 'name_', 'name', 'description', 'image', 'date', 'pages', 'old_price', 'new_price',
                  'description_', 'hashtag', 'category', 'country', 'status',
                  'similars', 'author', 'demo', 'content_data'
                  )
        read_only_fields = ('date', 'status', 'similars', 'new_price')
        depth = 1

    def to_representation(self, instance):
        data = super(ResearchSerializer, self).to_representation(instance)
        data.pop('image')
        data.pop('demo')
        data['image'] = instance.clean_image_path
        data['demo'] = instance.clean_demo_path
        return data


class ResearchUploadSerializer(serializers.ModelSerializer):
    hashtag = HashtagSerializer(many=True, required=False)
    country = CountrySerializer(many=True, required=False)
    name_ = serializers.ReadOnlyField(source='get_name')
    description_ = serializers.ReadOnlyField(source='get_description')
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    author = AboutMeSection(read_only=True)
    research_data = ResearchFilePathSerializer(read_only=True, many=True)
    similars = CardResearchSerializer(source='similar_researches', many = True, read_only=True)
    content_data = serializers.CharField(write_only=True, required=False)

    def get_name(self):
        return _(self.name)

    def get_description(self):
        return _(self.name)

    class Meta:
        model = Research
        fields = '__all__'
        read_only_fields = ('date', 'status', 'similars', 'new_price')

    def create(self, validated_data):

        content_data_validated = validated_data.pop('content_data', ' ')
        research = Research.objects.create(author=self.context['request'].user.initial_reference, **validated_data)
        Statistics.objects.create(research_to_collect=research)

        files_of_research = self.context.get('request').FILES

        if content_data_validated is None:
            pass
        else:
            serialized_content_data = json.loads(content_data_validated)
            for main_language in serialized_content_data:
                r_content = ResearchContent.objects.create(content_data=research, **main_language)

        for file in files_of_research.values():
            ext = os.path.splitext(file.name)[1]
            if not ext.lower() in ['.pdf', '.doc', '.docx', '.jpg', '.png', '.xlsx', '.xls', '.csv', '.jpeg', '.ppt']:

                raise serializers.ValidationError("Неподдерживаемый тип данных")

            else:
                alphabet = string.ascii_letters + string.digits
                salt = ''.join(secrets.choice(alphabet) for i in range(16))
                salt += file.name
                a = ResearchFiles.objects.create(research=research, name=salt)

        hashtag_name = self.context.get('request').POST.get('hashtag', 'None')

        if not hashtag_name.isdigit():
            validated_data['hashtag'] = hashtag_name

            split_hashtags = hashtag_name.split(' ')
            for i in split_hashtags:
                try:
                    created = Hashtag.objects.get(name=i.replace(',', ''))
                    get_id_if_yes = created.id
                    add_if_yes = research.hashtag.add(get_id_if_yes)

                except ObjectDoesNotExist:
                    hashtag = research.hashtag.create(name=i.replace(',', ''))

        else:
            raise serializers.ValidationError({'detail': _("Hashtag can not contain digits.")})

        country_names = self.context.get('request').POST.get('country', 'None')
        if not country_names.isdigit():
            validated_data['country'] = country_names

            split_countries = country_names.split(' ')
            for country in split_countries:
                try:
                    created = Country.objects.get(name=country.replace(',', ''))
                    add_id_if_country_exists = created.id
                    add_if_true = research.country.add(add_id_if_country_exists)
                except ObjectDoesNotExist:
                    state = research.country.create(name=country.replace(',', ''))

        else:
            raise serializers.ValidationError({'detail': _("Countries can not contain digits.")})

        return research

    def to_representation(self, instance):
        data = super(ResearchUploadSerializer, self).to_representation(instance)
        cleaned_data = dict(data)
        cleaned_data.pop('comment')
        return cleaned_data


class DiscountPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Research
        fields = ['new_price']
