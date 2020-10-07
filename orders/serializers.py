from rest_framework import serializers
from research.models import Research
from .models import Orders, OrderForm


class OrderFormSerailizer(serializers.ModelSerializer):

    class Meta:
        model = OrderForm
        fields = ['name', 'logo', 'email', 'phone_number', 'description']

    def create(self, validated_data):
        order = OrderForm.objects.create(**validated_data)
        order.save()
        return order


class OrdersCreateSerializer(serializers.ModelSerializer):
    total = serializers.IntegerField(read_only=True)

    class Meta:
        model = Orders
        fields = ['customer', 'ordered_researches', 'total']
