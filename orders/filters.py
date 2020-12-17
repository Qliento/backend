from django_filters import rest_framework as filters
from .models import Statistics, StatisticsDemo, StatisticsBought, StatisticsWatches


class StatFilter(filters.FilterSet):
    demos_downloaded = filters.DateFromToRangeFilter(field_name='demos_downloaded__date', lookup_expr='iexact')
    watches_counted = filters.DateFromToRangeFilter(field_name='watches_counted__date', lookup_expr='iexact')
    bought_researches = filters.DateFromToRangeFilter(field_name='bought_researches__date', lookup_expr='iexact')

    class Meta:
        model = Statistics
        fields = ['demos_downloaded', 'watches_counted', 'bought_researches']


