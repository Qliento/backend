from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import *
from .models import *
from registration.models import QAdmins
from orders.models import Statistics, StatisticsWatches
from registration.utils import Util
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser


from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_multiple_model.views import ObjectMultipleModelAPIView


class FiltersAPIView(ObjectMultipleModelAPIView):
    permission_classes = (AllowAny,)
    pagination_class = None
    
    authors_query = QAdmins.objects.all()
    # authors_query = authors_query.annotate(count = Count("creator")).filter(count__gt=0, status = 2)
    querylist = [
        {'queryset': Category.objects.filter(parent = None), 'serializer_class': CategorySubCategory},
        {'queryset': Country.objects.all(), 'serializer_class': CountrySerializer},
        {'queryset': authors_query, 'serializer_class': AuthorSerializer}
    ]


class DefaultResearchView(APIView):
    permission_classes = [AllowAny, ]
    parser_classes = [MultiPartParser, FormParser]
    queryset = Research.objects.all()

    def get(self, request, format=None):
        research = Research.objects.order_by('-id').filter(status=2)
        serializer = ResearchSerializer(research, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UploadResearchView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = Research.objects.all()
    serializer_class = ResearchUploadSerializer
    parser_classes = (JSONParser, MultiPartParser)

    def post(self, request, *args, **kwargs):
        file_serializer = self.get_serializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            get_name_of_research = list(request.data.values())[0]
            email_body = 'Доброго времени суток, Qliento! \n' + \
                         'Партнер: {}, отправил вам запрос на одобрение своего исследования. \n' \
                         'Название исследования: "{}". \n' \
                         'Пройдите пожалуйста в админ-панель для принятия дальнейших действий.'.format(request.user.name, get_name_of_research)

            data = {'email_body': email_body, 'to_email': 'qlientoinfo@gmail.com',
                    'email_subject': 'Исследование на подтверждение'}
            Util.send_email(data)

            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResearchDetail(generics.RetrieveAPIView):
    permission_classes = [AllowAny, ]
    queryset = Research.objects.filter(status=2)
    serializer_class = CardResearchSerializer

    def retrieve(self, request, *args, **kwargs):
        b = Statistics.objects.get(research_to_collect=self.kwargs['pk'])
        a = StatisticsWatches.objects.create(count_watches=1, watches=b)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ResearchOfPartnerDetail(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = AdminCardResearchSerializer

    def get(self, request, *args, **kwargs):
        data_of_instance = Research.objects.get(id=self.kwargs['pk'], author=request.user.initial_reference)
        serializer = self.get_serializer(data_of_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateDiscountPrice(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = DiscountPriceSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(Research.objects.get(status=4, id=self.kwargs['pk'], author_id=self.request.user.initial_reference.id))
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        the_object = Research.objects.get(status=4, id=self.kwargs['pk'], author_id=self.request.user.initial_reference.id)
        serializer = self.serializer_class(the_object, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        email_body = 'Доброго времени суток, Qliento! \n' + \
                     'Партнер: {}, отправил вам запрос на одобрение скидочной цены своего исследования. \n' \
                     'Название исследования: "{}". \n' \
                     'Новая скидочная цена: "{}". \n' \
                     'Пройдите пожалуйста в админ-панель для принятия дальнейших действий.'.format(request.user.name,
                                                                                                   the_object.name,
                                                                                                   request.data.get('new_price'),
                                                                                                   )

        data = {'email_body': email_body, 'to_email': 'qlientoinfo@gmail.com',
                'email_subject': 'Цена исследования на подтверждение'}
        Util.send_email(data)
        return Response(serializer.data, status=status.HTTP_200_OK)
