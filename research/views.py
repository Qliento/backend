from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import *
from .models import *
from registration.models import QAdmins
from orders.models import Statistics
from registration.utils import Util
from rest_framework.parsers import MultiPartParser, FormParser


from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_multiple_model.views import ObjectMultipleModelAPIView


class FiltersAPIView(ObjectMultipleModelAPIView):
    permission_classes = (AllowAny,)
    pagination_class = None
    querylist = [
        {'queryset': Category.objects.filter(parent = None), 'serializer_class': CategorySubCategory},
        {'queryset': Country.objects.all(), 'serializer_class': CountrySerializer},
        {'queryset': QAdmins.objects.all(), 'serializer_class': AuthorSerializer}
    ]


class DefaultResearchView(APIView):
    permission_classes = [AllowAny, ]
    parser_classes = [MultiPartParser, FormParser]
    queryset = Research.objects.all()
    serializer_class = CardResearchSerializer
    
    def get(self, request, format=None):
        research = Research.objects.order_by('-id').filter(status=2)
        serializer = ResearchSerializer(research, many=True)
        del serializer.data[0]['research_data']
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UploadResearchView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = Research.objects.all()
    serializer_class = ResearchSerializer
    parser_classes = (JSONRenderer, MultiPartParser)

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


class UpdateResearchView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = Research.objects.all()
    serializer_class = ResearchUpdateSerializer

    def get(self, request, *args, **kwargs):
        self.queryset = Research.objects.filter(id=self.kwargs['pk'], author=request.user.initial_reference)
        return Response(data=list(self.queryset.values()), status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        try:
            my_queryset = Research.objects.filter(id=self.kwargs['pk'], author=request.user.initial_reference).update(new_price=request.data.get('new_price'))
            get_updated = Research.objects.filter(id=self.kwargs['pk'], author=request.user.initial_reference)
            name_of_research = list(get_updated.values())[0].get('name')
            email_body = 'Доброго времени суток, Qliento! \n' + \
                         'Партнер: {}, отправил вам запрос на одобрение скидочной цены своего исследования. \n' \
                         'Название исследования: "{}". \n' \
                         'Новая скидочная цена: "{}". \n'  \
                         'Пройдите пожалуйста в админ-панель для принятия дальнейших действий.'.format(request.user.name,
                                                                                                       name_of_research,
                                                                                                       request.data.get('new_price'),
                                                                                                       )

            data = {'email_body': email_body, 'to_email': 'qlientoinfo@gmail.com',
                    'email_subject': 'Цена исследования на подтверждение'}
            Util.send_email(data)

            return Response(list(get_updated.values())[0], status=status.HTTP_202_ACCEPTED)
        except ValueError:
            content = {'message': 'Убедитесь в том, что вы ввели целые числа'}
            return Response(content, status=status.HTTP_304_NOT_MODIFIED)


class ResearchDetail(generics.RetrieveAPIView):
    permission_classes = [AllowAny, ]
    queryset = Research.objects.filter(status = 2)
    serializer_class = ResearchSerializer


class UpdateDiscountPrice(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = DiscountPriceSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(Research.objects.get(status=3, id=self.kwargs['pk'], author_id=self.request.user.id))
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(Research.objects.get(status=3, id=self.kwargs['pk'], author_id=self.request.user.id), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
