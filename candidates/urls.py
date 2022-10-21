from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (CandidateFiles, CandidateViewset,
                    CandidateWithoutFullLocation, ConfirmFileUpload,
                    FileUpload, GetFilterData, ImageUploadView, LocationView,
                    SearchQueryView)

router = DefaultRouter()
router.register(r'without-location', CandidateWithoutFullLocation, basename='candidate-location')
router.register(r'location', LocationView, basename='location')
router.register(r'files', CandidateFiles, basename='files')
router.register(r'', CandidateViewset, basename='candidate')
router.register(r'images', ImageUploadView, basename='images')



urlpatterns = [
    path('confirm-file/', ConfirmFileUpload.as_view(), name='upload-file'),
    path('upload/', FileUpload.as_view(), name='upload-file'),
    path('get-filter-data', GetFilterData.as_view(), name='filter_data'),
    path('analytics/', SearchQueryView.as_view(), name='analytics')
    
]

urlpatterns += router.urls
