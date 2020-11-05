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
        queryset = self.queryset
        category = self.request.query_params.get(None, 'category')
        if category is None or category.isdigit() == False:
        	return Research.objects.all().order_by('-id')
        else:
        	return queryset.filter(category__parent=category).order_by('-id')
        return queryset

