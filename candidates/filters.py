from .models import Candidate
from django_filters import rest_framework as filters
from django.contrib.postgres.search import SearchQuery
from django.db import models



class CandidateFilter(filters.FilterSet):
    def __init__(self, *args, **kwargs):
        queryset = Candidate.objects.prefetch_related('location')
        kwargs['queryset'] = queryset
        super().__init__(*args, **kwargs)
    
    name = filters.CharFilter(field_name='name', lookup_expr='icontains', method='filter_name', distinct=True)
    state = filters.CharFilter(field_name='location__state',lookup_expr='icontains', distinct=True)
    state_code = filters.CharFilter(field_name='location__state_code', lookup_expr='icontains')
    senatorial_district = filters.CharFilter(field_name='location__senatorial_district', lookup_expr='icontains')
    senatorial_district_code = filters.CharFilter(field_name='location__senatorial_district_code',lookup_expr='icontains')
    federal_constituency = filters.CharFilter(field_name='location__federal_constituency', lookup_expr='icontains')
    federal_constituency_code = filters.CharFilter(field_name='location__federal_constituency_code',lookup_expr='icontains')
    state_constituency = filters.CharFilter(field_name='location__state_constituency',lookup_expr='icontains')
    state_constituency_code = filters.CharFilter(field_name='location__state_constituency_code',lookup_expr='icontains')
    lga = filters.CharFilter(field_name='location__lga',lookup_expr='icontains')
    lga_code = filters.CharFilter(field_name='location__lga_code',lookup_expr='icontains')
    ward = filters.CharFilter(field_name='location__ward',lookup_expr='icontains')
    ward_code = filters.CharFilter(field_name='location__ward_code',lookup_expr='icontains')
    polling_unit = filters.CharFilter(field_name='location__polling_unit',lookup_expr='icontains')
    polling_unit_code = filters.CharFilter(field_name='location__polling_unit_code',lookup_expr='icontains')
    party = filters.CharFilter(field_name='party__name',lookup_expr='icontains')
    year = filters.CharFilter(field_name='position__year',lookup_expr='icontains')
    position= filters.CharFilter(field_name='position__position__name',lookup_expr='icontains')
    min_age = filters.NumberFilter(field_name="age", lookup_expr='gte')
    max_age = filters.NumberFilter(field_name="age", lookup_expr='lte')
    
    
    def filter_queryset(self, queryset):
        return super(CandidateFilter, self).filter_queryset(queryset).distinct()
    
    def filter_queryset(self, queryset):
        """
        Filter the queryset with the underlying form's `cleaned_data`. You must
        call `is_valid()` or `errors` before calling this method.

        This method should be overridden if additional filtering needs to be
        applied to the queryset before it is cached.
        """
        for name, value in self.form.cleaned_data.items():
            queryset = self.filters[name].filter(queryset, value).prefetch_related('location')
            assert isinstance(
                queryset, models.QuerySet
            ), "Expected '%s.%s' to return a QuerySet, but got a %s instead." % (
                type(self).__name__,
                name,
                type(queryset).__name__,
            )
        return queryset
    

    class Meta:
        model = Candidate
        # fields = [ 'name',  'min_age', 'max_age', 'gender', 'location']
        fields = ['name', 'min_age', 'max_age' ,'gender', 'qualifications', 'location', 'party', 'state', 'senatorial_district', 'federal_constituency', 
                  'state_constituency','lga','ward','polling_unit','position','year','state_code','senatorial_district_code','federal_constituency_code',
                  'state_constituency_code','lga_code','ward_code','polling_unit_code']
        
    def filter_name(self, queryset, name, value):
        splitted_name = value.split()
        result = queryset
        for m in range(0, len(splitted_name)):
            result = result.filter(name__icontains=splitted_name[m])
        return result