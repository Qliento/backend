from itertools import chain
from rest_framework import serializers
from research.models import Research
from .models import Orders, OrderForm, Cart, DemoVersionForm, Instructions, Statistics, \
    ShortDescriptions, StatisticsDemo, Check
from collections import OrderedDict
from rest_framework import request
from registration.models import QAdmins
from research.serializers import Country, Hashtag, CardResearchSerializer


def to_dict(instance):
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
        data[f.name] = f.value_from_object(instance)
    for f in opts.many_to_many:
        data[f.name] = [i.email for i in f.value_from_object(instance)]
    return data


class CartedItemsSerializer(serializers.ModelSerializer):
    ordered_items = CardResearchSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = "__all__"
        depth = 2

    def to_representation(self, instance):
        data = super(CartedItemsSerializer, self).to_representation(instance)
        cleaned_data = dict(data)
        cleaned_data.pop('buyer')
        return cleaned_data


class ItemsInCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = "__all__"
        depth = 1

    def to_representation(self, instance):
        data = super(ItemsInCartSerializer, self).to_representation(instance)
        cleaned_data = dict(data)
        cleaned_data.pop('buyer')
        return cleaned_data


class AddToCartSerializer(serializers.ModelSerializer):
    count_items = serializers.CharField(read_only=True)
    get_discount = serializers.CharField(read_only=True)
    get_general_sum = serializers.CharField(read_only=True)
    ordered_item = serializers.PrimaryKeyRelatedField(many=True, queryset=Research.objects.all())

    class Meta:
        model = Cart
        fields = ['id', 'count_items', 'get_discount', 'get_general_sum', 'ordered_item']

    def create(self, validated_data):

        ordered_thin = validated_data.pop('ordered_item')
        cart_general = Cart.objects.create(buyer=self.context['request'].user,
                                           **validated_data)
        for i in ordered_thin:
            cart_general.ordered_item.add(i)

        return cart_general

    def to_representation(self, instance):

        if instance:
            serializer = ItemsInCartSerializer(instance)

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

    def create(self, validated_data):
        demo_validated = validated_data.pop('desired_research')
        a = StatisticsDemo.objects.create(count_demo=1)
        b = Statistics.objects.filter(research_to_collect=demo_validated)
        b.update(demo_downloaded=a)
        demo = DemoVersionForm.objects.create(desired_research=demo_validated, **validated_data)
        return demo


class MyOrdersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Check
        fields = ['ordered_researches', 'date', 'id']

    def to_representation(self, instance):
        data = super(MyOrdersSerializer, self).to_representation(instance)
        research_details = []
        get_cleaned_data = dict(data).get('ordered_researches')[0]

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
        fields = ['title', 'picture1', 'text1']


class StatisticsSerializer(serializers.ModelSerializer):
    partner_admin = serializers.PrimaryKeyRelatedField(queryset=QAdmins.objects.all())

    class Meta:
        model = Statistics
        fields = '__all__'
