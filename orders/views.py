from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListCreateAPIView, ListAPIView, RetrieveDestroyAPIView, GenericAPIView
from rest_framework.response import Response
from .serializers import OrderFormSerailizer, OrdersCreateSerializer, \
    MyOrdersSerializer, CartedItemsSerializer, AddToCartSerializer, EmailDemoSerializer, ShortDescriptionsSerializer
from .models import OrderForm, Orders, Cart, ShortDescriptions, DemoVersionForm
from registration.models import Users, Clients
from rest_framework.permissions import AllowAny, IsAuthenticated
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
        self.queryset = Orders.objects.filter(items_ordered__buyer=request.user)
        return self.list(request, *args, **kwargs)


class ItemInCartView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CartedItemsSerializer
    queryset = None

    def get(self, request, *args, **kwargs):
        self.queryset = Cart.objects.filter(buyer=request.user.id)
        return self.list(request, *args, **kwargs)


class ItemCartDeleteView(RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CartedItemsSerializer
    queryset = None

    def destroy(self, request, *args, **kwargs):
        instance = Cart.objects.filter(buyer=request.user.id, id=self.kwargs['pk'])
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddToCartView(CreateAPIView):
    queryset = Cart.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = AddToCartSerializer


class SendDemoView(CreateAPIView):
    queryset = DemoVersionForm.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = EmailDemoSerializer


class ShortDescriptionView(ListAPIView):
    queryset = ShortDescriptions.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ShortDescriptionsSerializer
