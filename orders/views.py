from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListCreateAPIView, DestroyAPIView
from .serializers import OrderFormSerailizer, OrdersCreateSerializer
from .models import OrderForm, Orders
from rest_framework.permissions import AllowAny, IsAuthenticated
# Create your views here.


class OrderFormCreateView(CreateAPIView):
    queryset = OrderForm.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = OrderFormSerailizer


class OrderCreateView(ListCreateAPIView):
    queryset = Orders.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = OrdersCreateSerializer
