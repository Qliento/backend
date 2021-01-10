from itertools import chain
from rest_framework import serializers
from research.models import Research
from .models import Orders, OrderForm, Cart, DemoVersionForm, Statistics, \
    ShortDescriptions, StatisticsDemo, Check, StatisticsBought, StatisticsWatches, StatisticsDemo
from collections import OrderedDict
from django.utils.translation import ugettext_lazy as _
from django.db.models import Sum, Count
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

        demo_num = 0
        watches_num = 0
        bought_num = 0

        day = datetime.date.today().day
        month = datetime.date.today().month
        year = datetime.date.today().year

        today = '{}-{}-{}'.format(year, month, day+1)

        if self.context.get('choice') == 1:
            for stat_info in find_stat:
                demo_num = StatisticsDemo.objects.filter(demo_downloaded=stat_info.id,
                                                         date__day=datetime.date.today().day).aggregate(Count('count_demo'))
                watches_num = StatisticsWatches.objects.filter(watches=stat_info.id,
                                                               date__day=datetime.date.today().day).aggregate(Count('count_watches'))
                bought_num = StatisticsBought.objects.filter(bought=stat_info.id,
                                                             date__day=datetime.date.today().day).aggregate(Count('count_purchases'))
        if self.context.get('choice') == 2:
            for stat_info in find_stat:
                demo_num = StatisticsDemo.objects.filter(demo_downloaded=stat_info.id,
                                                         date__range=['{}-{}-{}'.format(year, month, day-7), today]).aggregate(Count('count_demo'))
                watches_num = StatisticsWatches.objects.filter(watches=stat_info.id,
                                                               date__range=['{}-{}-{}'.format(year, month, day-7), today]).aggregate(Count('count_watches'))
                bought_num = StatisticsBought.objects.filter(bought=stat_info.id,
                                                             date__range=['{}-{}-{}'.format(year, month, day-7), today]).aggregate(Count('count_purchases'))
        if self.context.get('choice') == 3:
            for stat_info in find_stat:
                demo_num = StatisticsDemo.objects.filter(demo_downloaded=stat_info.id,
                                                         date__range=['{}-{}-{}'.format(year, month-1, day), today]).aggregate(Count('count_demo'))
                watches_num = StatisticsWatches.objects.filter(watches=stat_info.id,
                                                               date__range=['{}-{}-{}'.format(year, month-1, day), today]).aggregate(Count('count_watches'))
                bought_num = StatisticsBought.objects.filter(bought=stat_info.id,
                                                             date__range=['{}-{}-{}'.format(year, month-1, day), today]).aggregate(Count('count_purchases'))
        if self.context.get('choice') == 4:
            for stat_info in find_stat:
                demo_num = StatisticsDemo.objects.filter(demo_downloaded=stat_info.id,
                                                         date__range=['{}-{}-{}'.format(year-1, month, day), today]).aggregate(Count('count_demo'))
                watches_num = StatisticsWatches.objects.filter(watches=stat_info.id,
                                                               date__range=['{}-{}-{}'.format(year-1, month, day), today]).aggregate(Count('count_watches'))
                bought_num = StatisticsBought.objects.filter(bought=stat_info.id,
                                                             date__range=['{}-{}-{}'.format(year-1, month, day), today]).aggregate(Count('count_purchases'))
        if self.context.get('choice') == 5:
            for stat_info in find_stat:
                demo_num = StatisticsDemo.objects.filter(demo_downloaded=stat_info.id).aggregate(Count('count_demo'))
                watches_num = StatisticsWatches.objects.filter(watches=stat_info.id).aggregate(Count('count_watches'))
                bought_num = StatisticsBought.objects.filter(bought=stat_info.id).aggregate(Count('count_purchases'))

        return {"demos_downloaded": demo_num.get('count_demo__count'),
                "watches": watches_num.get('count_watches__count'),
                "bought": bought_num.get('count_purchases__count')}


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

        researches_from_cart = Cart.objects.filter(user_cart=instance.id, added=False)
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
    ordered_researches = CardResearchSerializer(many=True, read_only=True)

    class Meta:
        model = Check
        fields = ['ordered_researches']

    def to_representation(self, instance):
        data = super(MyOrdersSerializer, self).to_representation(instance)
        return dict(data).get('ordered_researches')[0]


class ShortDescriptionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShortDescriptions
        fields = ['title', 'picture1', 'text1']


class BoughtByUser(serializers.ModelSerializer):

    class Meta:
        model = Research
        fields = ['image', 'name', 'description', 'pages', 'hashtag', 'country', 'new_price', 'id']

    def to_representation(self, instance):
        data = super(BoughtByUser, self).to_representation(instance)
        data.pop('image')
        data['image'] = instance.clean_image_path
        return data


class EmailDemoSerializer(serializers.ModelSerializer):
    desired_research = serializers.PrimaryKeyRelatedField(queryset=Research.objects.all())

    class Meta:
        fields = "__all__"
        model = DemoVersionForm

    def create(self, validated_data):
        demo_validated = validated_data.pop('desired_research')
        b = Statistics.objects.get(research_to_collect=demo_validated)
        a = StatisticsDemo.objects.create(count_demo=1, demo_downloaded=b)
        demo = DemoVersionForm.objects.create(desired_research=demo_validated, **validated_data)
        return demo


class OrderFormSerailizer(serializers.ModelSerializer):

    class Meta:
        model = OrderForm
        fields = ['name', 'surname', 'logo', 'email', 'phone_number', 'description']

    def create(self, validated_data):
        order = OrderForm.objects.create(**validated_data)
        return order


'pg_order_id = 10 & pg_payment_id = 401986682 & pg_salt = T1d4wSwresf6uBwR & pg_sig = 6 bdc59bf69bb0200103bb4475a99680a'


