from itertools import chain
from rest_framework import serializers
from research.models import Research
from .models import Orders, OrderForm, Cart, DemoVersionForm, ShortDescriptions, Statistics
from collections import OrderedDict
from rest_framework import request
from registration.models import QAdmins
from research.serializers import Country, Hashtag


def to_dict(instance):
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
        data[f.name] = f.value_from_object(instance)
    for f in opts.many_to_many:
        data[f.name] = [i.email for i in f.value_from_object(instance)]
    return data


class CartedItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"


class AddToCartSerializer(serializers.ModelSerializer):
    count_items = serializers.CharField(read_only=True)
    get_discount = serializers.CharField(read_only=True)
    get_general_sum = serializers.CharField(read_only=True)
    ordered_items = serializers.PrimaryKeyRelatedField(queryset=Research.objects.all())

    class Meta:
        model = Cart
        fields = ['id', 'count_items', 'get_discount', 'get_general_sum', 'ordered_items']

    def create(self, validated_data):
        ordered_thin = validated_data.pop('ordered_items')
        cart_general = Cart.objects.create(buyer=self.context['request'].user, ordered_item=ordered_thin, **validated_data)
        cart_general.amount_of_items = cart_general.count_items
        cart_general.discount = cart_general.get_discount
        cart_general.total_of_all = cart_general.get_general_sum['new_price__sum']
        cart_general.save(update_fields=['amount_of_items'])
        cart_general.save(update_fields=['discount'])
        cart_general.save(update_fields=['total_of_all'])
        return cart_general

    def to_representation(self, instance):
        if instance:
            serializer = CartedItemsSerializer(instance)
            return serializer.data
        else:
            raise Exception('Something went wrong...')


class OrderFormSerailizer(serializers.ModelSerializer):

    class Meta:
        model = OrderForm
        fields = ['name', 'surname', 'logo', 'email', 'phone_number', 'description']

    def create(self, validated_data):
        order = OrderForm.objects.create(**validated_data)
        return order


class OrdersCreateSerializer(serializers.ModelSerializer):
    get_total_from_cart = serializers.IntegerField(read_only=True)
    items_ordered = serializers.PrimaryKeyRelatedField(many=True, queryset=Cart.objects.all())

    class Meta:
        model = Orders
        fields = "__all__"
        depth = 2


class BoughtByUser(serializers.ModelSerializer):

    class Meta:
        model = Research
        fields = ['image', 'name', 'description', 'pages', 'hashtag', 'country', 'new_price', 'id']


class EmailDemoSerializer(serializers.ModelSerializer):
    desired_research = serializers.PrimaryKeyRelatedField(queryset=Research.objects.all())

    class Meta:
        fields = "__all__"
        model = DemoVersionForm


class MyOrdersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Orders
        fields = ['items_ordered', 'date_added', 'completed']

    def to_representation(self, instance):
        data = super(MyOrdersSerializer, self).to_representation(instance)
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


class ShortDescriptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortDescriptions
        fields = ['picture1', 'text1', 'picture2', 'text2']


class StatisticsSerializer(serializers.ModelSerializer):
    partner_admin = serializers.PrimaryKeyRelatedField(queryset=QAdmins.objects.all())

    class Meta:
        model = Statistics
        fields = '__all__'

