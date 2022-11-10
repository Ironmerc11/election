from django.contrib import admin
from .models import Candidate, Location, Position, RunningPosition, CandidateFile,Party, SearchQuery



# class CandidateFilter(UserAdmin):
#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         (_('Personal info'), {'fields': ('first_name', 'last_name')}),
#         (_('Permissions'), {
#             'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
#         }),
#         (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'password1', 'password2'),
#         }),
#     )
#     list_display = ('email', 'first_name', 'last_name', 'is_staff')
#     list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
#     search_fields = ('email', 'first_name', 'last_name')
#     ordering = ('email',)
#     filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(Candidate)
admin.site.register(Location)
admin.site.register(Position)
admin.site.register(RunningPosition)
admin.site.register(CandidateFile)
admin.site.register(SearchQuery)
admin.site.register(Party)
