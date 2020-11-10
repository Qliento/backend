from rest_framework import serializers
from research.models import Research

from .models import Orders, OrderForm
from .models import Orders, OrderForm, Cart, DemoVersionForm, Instructions, Statistics, ShortDescriptions
from collections import OrderedDict
from rest_framework import request


class OrderFormSerailizer(serializers.ModelSerializer):

    class Meta:
        model = OrderForm
        fields = ['name', 'surname', 'logo', 'email', 'phone_number', 'description']

    def create(self, validated_data):
        order = OrderForm.objects.create(**validated_data)
        order.save()
        return order


class OrdersCreateSerializer(serializers.ModelSerializer):
    get_total = serializers.IntegerField(read_only=True)

    class Meta:
        model = Orders
        fields = ['customer', 'ordered_researches', 'get_total']

    def create(self, validated_data):
        special_total = Orders.objects.create(**validated_data)
        special_total.total = special_total.get_total
        special_total.save(update_fields=['total'])
        return special_total


class BoughtByUser(serializers.ModelSerializer):

    class Meta:
        model = Research
        fields = ['image', 'name', 'description', 'pages', 'hashtag', 'country', 'new_price', 'id']


class MyOrdersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Orders
        fields = ['ordered_researches', 'date_added', 'completed']
        depth = 2

    def to_representation(self, instance):
        data = super(MyOrdersSerializer, self).to_representation(instance)
        removed_fields = []
        retrieved_values = dict(data)
        ordered_researches_data = retrieved_values['ordered_researches']
        retrieved_orders = dict(ordered_researches_data)
        unnecessary_values = ['category', 'old_price', 'demo', 'status', 'research', 'similars']
        for i in retrieved_orders.items():
            if i[0] not in unnecessary_values:
                removed_fields.append(i)
        return OrderedDict(removed_fields)
        research_details = []
        get_cleaned_data = dict(data).get('items_ordered')[0]

        get_filtered_researches = Research.objects.filter(id=get_cleaned_data)
        data_for_filtering = list(get_filtered_researches.values())[0]
        fields_to_add = ['image', 'author_id', 'name', 'description', 'date', 'pages',
                  'hashtag', 'country', 'new_price', 'old_price', 'id']

        get_cleaned_countries = Country.objects.filter(research=get_cleaned_data)
        country_data_for_filtering = list(get_cleaned_countries.values("name"))

        get_cleaned_hashtags = Hashtag.objects.filter(research=get_cleaned_data)
        hashtag_data_for_filtering = list(get_cleaned_hashtags.values("name"))

        for i in data_for_filtering.items():
            if i[0] in fields_to_add:
                research_details.append(i)

        list_of_distinct = []

        for distinct_country in country_data_for_filtering:
            get_its_value = distinct_country.get('name')
            list_of_distinct.append(get_its_value)
            country_result = ("country", list_of_distinct,)
            research_details.append(country_result)

        list_of_distinct_hashtags = []

        for distinct_hashtag in hashtag_data_for_filtering:
            get_hashtag_value = distinct_hashtag.get('name')
            list_of_distinct_hashtags.append(get_hashtag_value)
            hashtag_result = ("hashtag", list_of_distinct_hashtags,)
            research_details.append(hashtag_result)

        return OrderedDict(research_details)


class InstructionSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShortDescriptions
        fields = "__all__"


class ShortDescriptionsSerializer(serializers.ModelSerializer):
    data_for_instructions = InstructionSerializer(many=True)

    class Meta:
        model = ShortDescriptions
        fields = '__all__'


class StatisticsSerializer(serializers.ModelSerializer):
    partner_admin = serializers.PrimaryKeyRelatedField(queryset=QAdmins.objects.all())

    class Meta:
        model = Statistics
        fields = '__all__'

