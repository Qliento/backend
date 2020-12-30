from .models import Research
from .serializers import CardResearchSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django_filters  import rest_framework as filters
from rest_framework.permissions import AllowAny
from django.db.models import Q
from .models import Category
from django.core.exceptions import ObjectDoesNotExist


class ResearchFilter(filters.FilterSet):

    class Meta:
        model = Research
        fields = {
            'country__name': ['icontains'],
            'category__name': ['iexact'],
            'hashtag__name': ['icontains'],
            'author__logo': ['icontains'],
            'name': ['icontains'],
        }


class ResearchViewSet(viewsets.ModelViewSet):
    queryset = Research.objects.filter(status = 2).order_by('-id')
    serializer_class = CardResearchSerializer
    permission_classes = [AllowAny, ]

    filter_fields=('country', 'category', 'hashtag', 'author', 'name')
    filterset_class = ResearchFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category', None)
        if category is None:
            return queryset
        else:
            return queryset.filter(status = 2, category__parent__name=category).order_by('-id')