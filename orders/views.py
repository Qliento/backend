from rest_framework.decorators import api_view, permission_classes
import hashlib
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListCreateAPIView, ListAPIView, RetrieveDestroyAPIView, RetrieveAPIView
from rest_framework.response import Response
from .serializers import OrderFormSerailizer, OrdersCreateSerializer, \
    MyOrdersSerializer, DeleteCartedItemSerializer, AddToCartSerializer, \
    EmailDemoSerializer, StatisticsSerializer, ShortDescriptionsSerializer, \
    ItemsInCartSerializer
from .models import OrderForm, Orders, Cart, ShortDescriptions, DemoVersionForm, Statistics, Check
from registration.models import Users, Clients
from rest_framework.permissions import AllowAny, IsAuthenticated
import secrets
import string
import hashlib

from django.http import HttpResponseRedirect


class OrderFormCreateView(CreateAPIView):
    queryset = OrderForm.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = OrderFormSerailizer


class OrderCreateView(ListCreateAPIView):
    queryset = Orders.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = OrdersCreateSerializer

    def create(self, request, *args, **kwargs):
        instances = Cart.objects.filter(buyer=request.user.id, id=request.data.get('items_ordered')[0]).update(added=True)
        response = super().create(request, *args, **kwargs)
        alphabet = string.ascii_letters + string.digits
        salt = ''.join(secrets.choice(alphabet) for i in range(16))

        str2hash = "payment.php;{};USD;test;ru;534270;{};vwc90Vew0ZJVxUfa".format(response.data['get_total_from_cart'], salt)
        result = hashlib.md5(str2hash.encode())
        md5result = result.hexdigest()

        return HttpResponseRedirect(
            redirect_to='https://api.paybox.money/payment.php?pg_merchant_id=534270&pg_amount={}&pg_currency=USD&pg_description=test&pg_salt={}&pg_language=ru&pg_sig'
                        '={}'.format(response.data['get_total_from_cart'], salt, md5result))


class MyOrdersView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MyOrdersSerializer
    queryset = None

    def get(self, request, *args, **kwargs):
        self.queryset = Check.objects.filter(client_bought=request.user.email)
        return self.list(request, *args, **kwargs)


class ItemInCartView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ItemsInCartSerializer
    queryset = None

    def get(self, request, *args, **kwargs):
        self.queryset = Orders.objects.filter(buyer=request.user.id)
        return self.list(request, *args, **kwargs)


class ItemCartDeleteView(RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = DeleteCartedItemSerializer
    queryset = None

    def destroy(self, request, *args, **kwargs):
        Cart.objects.filter(user_cart__buyer=self.request.user.id, ordered_item=self.kwargs['pk']).delete()
        return Response({"detail": _("Research was removed from your cart")}, status=status.HTTP_200_OK)


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


class StatViewForResearch(RetrieveAPIView):
    queryset = None
    permission_classes = (IsAuthenticated,)
    serializer_class = StatisticsSerializer

    def get(self, request, *args, **kwargs):
        self.queryset = Statistics.objects.filter(Q(partner_admin=request.user.initial_reference, partner_admin__creator__id=self.kwargs['exact_research']))
        return Response(list(self.queryset.values())[0], status=status.HTTP_200_OK)
