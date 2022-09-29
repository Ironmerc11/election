from .models import User
from django_filters import rest_framework as filters

class UserFilter(filters.FilterSet):  
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')

    class Meta:
        model = User
        fields = ['is_superuser', 'is_staff', 'email', 'verified', 'is_active', 'name']
        