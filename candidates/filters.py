from .models import Candidate
from django_filters import rest_framework as filters

class CandidateFilter(filters.FilterSet):
    location__year = filters.CharFilter(lookup_expr='icontains')
    location__state = filters.CharFilter(lookup_expr='icontains')
    location__state_code = filters.CharFilter(lookup_expr='icontains')
    location__senatorial_district = filters.CharFilter(lookup_expr='icontains')
    location__senatorial_district_code = filters.CharFilter(lookup_expr='icontains')
    location__federal_constituency = filters.CharFilter(lookup_expr='icontains')
    location__federal_constituency__code = filters.CharFilter(lookup_expr='icontains')
    location__state_constituency = filters.CharFilter(lookup_expr='icontains')
    location__state_constituency_code = filters.CharFilter(lookup_expr='icontains')
    location__lga = filters.CharFilter(lookup_expr='icontains')
    location__lga_code = filters.CharFilter(lookup_expr='icontains')
    location__ward = filters.CharFilter(lookup_expr='icontains')
    location__ward_code = filters.CharFilter(lookup_expr='icontains')
    location__polling_unit = filters.CharFilter(lookup_expr='icontains')
    location__polling_unit_code = filters.CharFilter(lookup_expr='icontains')
    party = filters.CharFilter(lookup_expr='icontains')
    name = filters.CharFilter(lookup_expr='icontains')
    position__year = filters.CharFilter(lookup_expr='icontains')
    position__position__name = filters.CharFilter(lookup_expr='icontains')
    min_age = filters.NumberFilter(field_name="age", lookup_expr='gte')
    max_age = filters.NumberFilter(field_name="age", lookup_expr='lte')
    
    
    

    class Meta:
        model = Candidate
        fields = ['name', 'min_age', 'max_age' ,'gender', 'qualifications', 'location', 'party', 'position']