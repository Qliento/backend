from rest_framework.decorators import api_view, permission_classes
import hashlib
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListCreateAPIView, ListAPIView, RetrieveDestroyAPIView, RetrieveAPIView, GenericAPIView
from rest_framework.response import Response
from .serializers import OrderFormSerailizer, OrdersCreateSerializer, \
    MyOrdersSerializer, DeleteCartedItemSerializer, AddToCartSerializer, \
    EmailDemoSerializer, StatisticsSerializer, ShortDescriptionsSerializer, \
    ItemsInCartSerializer
from .models import OrderForm, Orders, Cart, ShortDescriptions, DemoVersionForm, Statistics, Check, StatisticsBought
from research.models import Research
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
        get_order_id = Orders.objects.get(buyer=request.user.id)
        get_total_from_cart = get_order_id.get_total_from_cart

        # for i in request.data.get('items_ordered'):
        #     items_cart = Research.objects.get(id=i)
        #     instances = Cart.objects.filter(user_cart__buyer=request.user.id, ordered_item=items_cart, user_cart=get_order_id.id)
        #     instances.update(added=True)
        #     b = Statistics.objects.get(research_to_collect=items_cart.id)
        #     a = StatisticsBought.objects.create(count_purchases=1, bought=b)

        # response = super().create(request, *args, **kwargs)
        alphabet = string.ascii_letters + string.digits
        salt = ''.join(secrets.choice(alphabet) for i in range(16))

        str2hash = "payment.php;{};USD;test;ru;534270;{};{};vwc90Vew0ZJVxUfa".format(get_total_from_cart, get_order_id.id, salt)
        result = hashlib.md5(str2hash.encode())
        md5result = result.hexdigest()

        return Response('https://api.paybox.money/payment.php?pg_merchant_id=534270&pg_amount={}&pg_currency=USD&pg_description=test&pg_language=ru&pg_order_id={}&pg_salt={}'
                        '&pg_sig={}'.format(get_total_from_cart, get_order_id.id, salt, md5result))


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
        queryset = Statistics.objects.filter(Q(research_to_collect__author=request.user.initial_reference, research_to_collect=self.kwargs['exact_research']))
        data_itself = list(queryset.values())[0]
        serializer = StatisticsSerializer(queryset, data=data_itself, context=self.kwargs)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@csrf_exempt
@permission_classes((AllowAny,))
def get_paybox_url(request):
    get_needed_order = Orders.objects.get(id=request.POST.get('pg_order_id'))
    if get_needed_order:
        get_needed_order.pg_payment_id = request.POST.get('pg_payment_id')
        get_needed_order.save()
    else:
        pass
    return Response('ok')



