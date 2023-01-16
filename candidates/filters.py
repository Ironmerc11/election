from django_filters import rest_framework as filters
from django_filters.widgets import CSVWidget

from .models import Candidate, Location


class CandidateFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains', method='filter_name', distinct=True)
    party = filters.CharFilter(field_name='party__name', lookup_expr='icontains')
    year = filters.CharFilter(field_name='position__year', lookup_expr='icontains')
    position = filters.CharFilter(field_name='position__position__name', lookup_expr='icontains')
    min_age = filters.NumberFilter(field_name="age", lookup_expr='gte')
    max_age = filters.NumberFilter(field_name="age", lookup_expr='lte')
    location = filters.ModelMultipleChoiceFilter(field_name='location', method='filter_location_ids', widget=CSVWidget,
                                                 queryset=Location.objects.all())

    def filter_location_ids(self, queryset, name, value):
        # print(queryset)
        idx = self.data.get('location', None)
        if idx and value:
            idx = set(idx.split(","))
            queryset = queryset.filter(location__id__in=idx)
        return queryset

    def filter_queryset(self, queryset):
        return super(CandidateFilter, self).filter_queryset(queryset).distinct()

    def filter_name(self, queryset, name, value):
        splitted_name = value.split()
        result = queryset
        for m in range(0, len(splitted_name)):
            result = result.filter(name__icontains=splitted_name[m])
        return result

    class Meta:
        model = Candidate
        fields = ['name', 'min_age', 'max_age', 'gender', 'qualifications', 'party', 'position', 'year', 'location']


class LocationFilter(filters.FilterSet):
    state = filters.CharFilter(field_name='state', lookup_expr='icontains', distinct=True)
    lga = filters.CharFilter(field_name='lga', lookup_expr='icontains', distinct=True)
    ward = filters.CharFilter(field_name='ward', lookup_expr='icontains', distinct=True)
    polling_unit = filters.CharFilter(field_name='polling_unit', lookup_expr='icontains', distinct=True)

    class Meta:
        model = Location
        fields = ['state', 'lga', 'ward', 'polling_unit']
