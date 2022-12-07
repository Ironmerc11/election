from .models import Candidate, Location
from django_filters import rest_framework as filters
from django.contrib.postgres.search import SearchQuery
from django.db import models



class CandidateFilter(filters.FilterSet):
    
    
    # def __init__(self, *args, **kwargs):
    #     queryset = Candidate.objects.prefetch_related('location').prefetch_related('position')
    #     kwargs['queryset'] = queryset
    #     super().__init__(*args, **kwargs)
    
    name = filters.CharFilter(field_name='name', lookup_expr='icontains', method='filter_name', distinct=True)
    state = filters.CharFilter(field_name='location__state',lookup_expr='icontains', distinct=True)
    lga = filters.CharFilter(field_name='location__lga',lookup_expr='icontains')
    ward = filters.CharFilter(field_name='location__ward',lookup_expr='icontains')
    polling_unit = filters.CharFilter(field_name='location__polling_unit',lookup_expr='icontains')
    party = filters.CharFilter(field_name='party__name',lookup_expr='icontains')
    year = filters.CharFilter(field_name='position__year',lookup_expr='icontains')
    position= filters.CharFilter(field_name='position__position__name',lookup_expr='icontains')
    min_age = filters.NumberFilter(field_name="age", lookup_expr='gte')
    max_age = filters.NumberFilter(field_name="age", lookup_expr='lte')
    
    
    # def filter_queryset(self, queryset):
    #     return super(CandidateFilter, self).filter_queryset(queryset).distinct()
    
    # def filter_queryset(self, queryset):
    #     """
    #     Filter the queryset with the underlying form's `cleaned_data`. You must
    #     call `is_valid()` or `errors` before calling this method.

    #     This method should be overridden if additional filtering needs to be
    #     applied to the queryset before it is cached.
    #     """
    #     clean_dict = {k: v for k, v in self.form.cleaned_data.items() if v}
    #     for name, value in clean_dict.items():
    #         # print(value)
    #         # lookup = "%s__%s" % (self.field_name, self.lookup_expr)
    #         # qs = self.get_method(qs)(**{lookup: value})
    #         if name == 'lga':                
    #             try:
    #                 lga_id = Location.objects.filter(lga__icontains=value)[0]
    #             except:
    #               return Candidate.objects.none()
    #             candidate_name = clean_dict.get('name')
    #             if candidate_name:
    #                 queryset = Candidate.objects.filter(location__id=lga_id.id, name__icontains=candidate_name)
    #             else:
    #                 queryset = Candidate.objects.filter(location__id=lga_id.id)   
    #         else:
    #             queryset = self.filters[name].filter(queryset, value).distinct().prefetch_related('location').prefetch_related('position')
    #         assert isinstance(
    #             queryset, models.QuerySet
    #         ), "Expected '%s.%s' to return a QuerySet, but got a %s instead." % (
    #             type(self).__name__,
    #             name,
    #             type(queryset).__name__,
    #         )
    #     return queryset
    

    def filter_name(self, queryset, name, value):
        splitted_name = value.split()
        result = queryset
        for m in range(0, len(splitted_name)):
            result = result.filter(name__icontains=splitted_name[m])
        return result
    
    class Meta:
        model = Candidate
        # fields = [ 'name',  'min_age', 'max_age', 'gender', 'location']
        fields = ['name', 'min_age', 'max_age' ,'gender', 'qualifications', 'party', 'state', 'lga','ward','polling_unit','position','year', 'location']
        



class LocationFilter(filters.FilterSet):
    
    
    class Meta:
        model = Location
        fields = ['state', 'lga', 'ward', 'polling_unit']