from rest_framework import serializers
from research.models import Research
from .models import Orders, OrderForm, Cart, ItemsInCart
from collections import OrderedDict
from rest_framework import request


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemsInCart
        fields = ["__all__"]
        depth = 1


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
        fields = "__all__"
        depth = 1

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
        order.save()
        return order


class OrdersCreateSerializer(serializers.ModelSerializer):
    # get_total = serializers.IntegerField(read_only=True)

    class Meta:
        model = Orders
        fields = ['customer', 'ordered_researches']

    # def create(self, validated_data):
    #     special_total = Orders.objects.create(**validated_data)
    #     special_total.total = special_total.get_total
    #     special_total.save(update_fields=['total'])
    #     return special_total


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
