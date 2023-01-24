from django.contrib import admin
from .models import Candidate, Location, Position, RunningPosition, CandidateFile,Party, SearchQuery, ExcelFileData



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


class LocationAdmin(admin.ModelAdmin):
    model = Location
    list_display = ['polling_unit','polling_unit_code', 'ward', 'lga', 'state', 'year']
    list_filter = ['state', 'year']
    search_fields = ['polling_unit','polling_unit_code', 'ward', 'lga', 'state', 'year']


class CandidateFileAdmin(admin.ModelAdmin):
    model = CandidateFile
    list_display = ['id', 'file','uploaded_at', 'type', 'status', 'year']
    list_filter = ['type', 'uploaded_at', 'status']


class SearchQueryAdmin(admin.ModelAdmin):
    model = SearchQuery
    list_display = ['filter_combo', 'created_at', 'updated_at']


class CandidateAdmin(admin.ModelAdmin):
    model = Candidate
    list_display = ['name', 'party', 'gender', 'age', 'created_at', 'updated_at']
    list_filter = ['party', 'gender', 'age', 'created_at', 'updated_at']

# class LocationAdmin(admin.ModelAdmin):
    
#     # model = Location
#     # list_display = ['state', 'lga', 'ward', 'polling_unit', 'polling_unit_code']
#     # search_fields = ['polling_unit_code', 'state']
    

class ExcelFileAdmin(admin.ModelAdmin):
    model = ExcelFileData
    list_display = ['file_name', 'file_type', 'updated_at', 'created_at']

    
admin.site.register(Candidate, CandidateAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Position)
admin.site.register(RunningPosition)
admin.site.register(CandidateFile, CandidateFileAdmin)
admin.site.register(SearchQuery, SearchQueryAdmin)
admin.site.register(Party)
admin.site.register(ExcelFileData, ExcelFileAdmin)
