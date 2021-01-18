from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
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
from research.models import Research, ResearchFiles
from rest_framework.permissions import AllowAny, IsAuthenticated
import secrets
import string
import hashlib
from registration.utils import Util
import zipfile
from qliento import settings
import datetime
from django.core.mail import EmailMessage
from io import StringIO
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (Mail, Attachment, FileContent, FileName, FileType, Disposition)
from rest_framework.parsers import MultiPartParser
from django.http import FileResponse, HttpResponseRedirect
import base64
import jwt
from registration.models import Users
from rest_framework.exceptions import AuthenticationFailed


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

        alphabet = string.ascii_letters + string.digits
        salt = ''.join(secrets.choice(alphabet) for i in range(16))
        param1 = ''.join(secrets.choice(alphabet) for i in range(16))

        description = ''

        for i in request.data.get('items_ordered'):
            items_cart = Research.objects.get(id=i)
            instances = Cart.objects.filter(user_cart__buyer=request.user.id, ordered_item=items_cart, user_cart=get_order_id.id)
            get_name = list(instances.values('ordered_item__name'))[0]['ordered_item__name']
            description += ' ID: {},'.format(i)
            description += ' Название исследования: {}.'.format(get_name)

        str2hash = "payment.php;{};USD;{};ru;534270;{};{};{};{};vwc90Vew0ZJVxUfa".format(get_total_from_cart, description, get_order_id.id, param1, salt, request.user.email)
        result = hashlib.md5(str2hash.encode())
        md5result = result.hexdigest()

        zeo = []
        search_id = 'ID:, 2020, Название, исследования:, 230, name.'
        for i in search_id.split():
            try:
                s = i.replace(',', '')
                zeo.append(int(s))
            except:
                pass

        get_order_id.pg_sig = param1
        get_order_id.save()

        return Response('https://api.paybox.money/payment.php?pg_merchant_id=534270&pg_amount={}&pg_currency=USD&pg_description={}&'
                        'pg_language=ru&pg_order_id={}&pg_param1={}&pg_salt={}&pg_user_contact_email={}'
                        '&pg_sig={}'.format(get_total_from_cart, description,
                                            get_order_id.id, param1, salt, request.user.email, md5result))


@api_view(["POST"])
@csrf_exempt
@permission_classes((AllowAny,))
def get_paybox_url(request):
    get_needed_order = Orders.objects.get(id=request.POST.get('pg_order_id'))
    get_the_buyer = request.POST.get('pg_user_contact_email')
    list_of_ids = []

    if get_needed_order:

        email_body = \
                     'Доброго времени суток, пользователь. ' + \
                     'Вам были отправлены файлы исследования. \n' + \
                     'Спасибо за покупку,\n' + \
                     'С уважением, команда Qliento'

        send_files = Mail(
            from_email='qlientoinfo@gmail.com',
            to_emails=[get_the_buyer],
            subject='Файлы исследования',
            html_content=email_body,
        )

        check_created = Check.objects.create(total_price=request.POST.get('pg_amount'),
                                             date=datetime.datetime.now(),
                                             client_bought=get_the_buyer,
                                             order_id=request.POST.get('pg_order_id'),
                                             pg_payment_id=request.POST.get('pg_payment_id')
                                             )

        for search_id in request.POST.get('pg_description').split():
            try:
                s = search_id.replace(',', '')
                list_of_ids.append(int(s))
            except:
                pass

        for i in list_of_ids:
            try:
                check_created.ordered_researches.add(Research.objects.get(id=i))
                check_created.save()
                Cart.objects.filter(added=False, user_cart=get_needed_order.id, ordered_item__id=i).update(added=True)
                files = Research.objects.filter(id=i).values('research_data')
                for each_file in files:

                    data_file = ResearchFiles.objects.get(id=each_file.get('research_data'))

                    with open('static/files/{}'.format(str(data_file)), 'rb') as f:
                        data = f.read()
                        f.close()

                    encoded_file = base64.b64encode(data).decode()

                    attachedFile = Attachment(
                        FileContent(encoded_file),
                        FileName(str(data_file)),
                        Disposition('attachment')
                    )

                    send_files.add_attachment = attachedFile

                    b = Statistics.objects.get(research_to_collect=i)
                    a = StatisticsBought.objects.create(count_purchases=1, bought=b)
            except:
                pass

        try:
            sg = SendGridAPIClient(settings.api_key)
            sg.send(send_files)

        except Exception as e:
            pass

    else:
        pass
    return Response('ok')


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


class DownloadZipView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = None
    parser_classes = [MultiPartParser]
    queryset = None

    def get(self, request, *args, **kwargs):
        token = self.kwargs.get('token')

        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = Users.objects.get(id=payload['user_id'])
            if user is None:
                raise AuthenticationFailed
            else:
                zip_file_name = 'files.zip'
                response = HttpResponse(content_type='application/x-zip-compressed')
                zipped_files = zipfile.ZipFile(response, 'w')

                try:
                    research_from_check = Check.objects.get(ordered_researches=self.kwargs.get('id'), client_bought=user.email)

                    for i in research_from_check.ordered_researches.all():
                        exact_files = ResearchFiles.objects.filter(research=i)

                        for exact_file in exact_files:
                            zipped_files.write('static/files/{}'.format(str(exact_file.name)))

                    zipped_files.close()
                    response['Content-Disposition'] = f'attachment; filename={zip_file_name}'

                    return response

                except IndexError:
                    content = {'message': 'Данное исследование не имеет файлов'}
                    return Response(content, status=400)

        except:
            pass


class DownloadFileView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = None
    parser_classes = [MultiPartParser]
    queryset = None

    def get(self, request, *args, **kwargs):
        token = request.headers.get('Authorization')[7:]
        return Response('https://back.qliento.com/purchase/zipped/{}/{}/'.format(self.kwargs.get('id'), token))

