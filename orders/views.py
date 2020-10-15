from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListCreateAPIView, GenericAPIView, ListAPIView
from rest_framework.response import Response

from .serializers import OrderFormSerailizer, OrdersCreateSerializer, MyOrdersSerializer
from .models import OrderForm, Orders
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
# Create your views here.


class OrderFormCreateView(CreateAPIView):
    queryset = OrderForm.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = OrderFormSerailizer


class OrderCreateView(ListCreateAPIView):
    queryset = Orders.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = OrdersCreateSerializer


class MyOrdersView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MyOrdersSerializer
    queryset = None

    def get(self, request, *args, **kwargs):
        self.queryset = Orders.objects.filter(customer=request.user.id)
        return self.list(request, *args, **kwargs)



