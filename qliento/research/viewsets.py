from .models import Research
from .serializers import ResearchSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django_filters  import rest_framework as filters


class ResearchFilter(filters.FilterSet):

    class Meta:
        model = Research
        fields = {
            'country__name': ['icontains'],
            'category__name': ['iexact'],
            'hashtag__name': ['icontains'],
        }


class ResearchViewSet(viewsets.ModelViewSet):
    queryset = Research.objects.filter(status = 2)
    serializer_class = ResearchSerializer
    filter_fields=('country', 'category', 'hashtag')
    filterset_class = ResearchFilter

