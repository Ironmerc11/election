from .models import User
from django_filters import rest_framework as filters

class UserFilter(filters.FilterSet):   

    class Meta:
        model = User
        fields = ['is_superuser', 'is_staff', 'first_name', 'last_name', 'email', 'verified', 'is_active']