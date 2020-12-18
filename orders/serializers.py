from itertools import chain
from rest_framework import serializers
from research.models import Research
from .models import Orders, OrderForm, Cart, DemoVersionForm, Statistics, \
    ShortDescriptions, StatisticsDemo, Check, StatisticsBought, StatisticsWatches, StatisticsDemo
from collections import OrderedDict
from django.utils.translation import ugettext_lazy as _
from django.db.models import Sum
from rest_framework import request
from registration.serializers import CustomValidation
from django.db.models import Q
from registration.models import QAdmins
from research.serializers import Country, Hashtag, CardResearchSerializer
from django.db.models.functions import Cast, TruncYear, TruncMonth, TruncDay
from django.db.models import DateTimeField
import  datetime
from django.utils import timezone


def to_dict(instance):
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
        data[f.name] = f.value_from_object(instance)
    for f in opts.many_to_many:
        data[f.name] = [i.email for i in f.value_from_object(instance)]
    return data


class StatisticsDemoSerializer(serializers.ModelSerializer):

    class Meta:
        model = StatisticsDemo
        fields = '__all__'


class StatisticsBoughtSerializer(serializers.ModelSerializer):

    class Meta:
        model = StatisticsBought
        fields = '__all__'


class StatisticsWatchesSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatisticsWatches
        fields = '__all__'


class StatisticsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Statistics
        fields = '__all__'

    def to_representation(self, instance):
        option = self.context.get('choice')
        the_instance_id = list(instance.values('id'))[0]
        find_stat = Statistics.objects.filter(id=the_instance_id.get('id'))

        for stat_info in find_stat:
            demo_num = StatisticsDemo.objects.filter(Q(demos_downloaded=stat_info.id,
                                                     date=datetime.date.today())).aggregate(Sum('count_demo'))

            # StatisticsWatches.objects.filter(watches_counted=stat_info.id)
            # StatisticsBought
            print(stat_info.id, StatisticsDemo.objects.filter(demos_downloaded=stat_info.id))
        data_for_stat = super(StatisticsSerializer, self).to_representation(instance)

        return data_for_stat


class AddToCartSerializer(serializers.ModelSerializer):
    ordered_item = serializers.PrimaryKeyRelatedField(queryset=Research.objects.filter(status=2))

    class Meta:
        model = Cart
        fields = ['ordered_item']

    def create(self, validated_data):
        item_added = None
        add_item_to_cart, created_order = Orders.objects.get_or_create(buyer=self.context['request'].user)

        if created_order:
            item_added, created = Cart.objects.get_or_create(user_cart=add_item_to_cart, **validated_data)
            if not created:
                raise CustomValidation(detail={"detail": _("Research is already in your cart")})
            else:
                item_added.total_of_all = item_added.calculate_total_price
                item_added.save()
        else:
            item_added, created = Cart.objects.get_or_create(user_cart=add_item_to_cart, **validated_data)
            if not created:
                raise CustomValidation(detail={"detail": _("Research is already in your cart")})
            else:
                item_added.total_of_all = item_added.calculate_total_price
                item_added.save()
        return item_added


class ItemsInCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Orders
        fields = ['id']
        depth = 1

    def to_representation(self, instance):
        instance.total_sum = instance.get_total_from_cart
        instance.save()

        researches_from_cart = Cart.objects.filter(user_cart=instance.id)
        list_of_researches = []
        price_of_total = 0
        nominal_total = researches_from_cart.aggregate(Sum('total_of_all'))

        for each_item in researches_from_cart:
            price_of_total += each_item.calculate_total_price
            needed_data = CardResearchSerializer(each_item.ordered_item).data
            list_of_researches.append(needed_data)

        if nominal_total.get('total_of_all__sum') != price_of_total:
            instance.total_sum = price_of_total
            instance.save()
        else:
            pass

        return {"ordered_items": list_of_researches,
                "total_sum": instance.total_sum}


class DeleteCartedItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = "__all__"
        depth = 2


class OrdersCreateSerializer(serializers.ModelSerializer):
    get_total_from_cart = serializers.ReadOnlyField()
    items_ordered = serializers.ReadOnlyField()

    class Meta:
        model = Orders
        fields = "__all__"


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


class OrderFormSerailizer(serializers.ModelSerializer):

    class Meta:
        model = OrderForm
        fields = ['name', 'surname', 'logo', 'email', 'phone_number', 'description']

    def create(self, validated_data):
        order = OrderForm.objects.create(**validated_data)
        return order
