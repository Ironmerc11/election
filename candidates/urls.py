from .views import CandidateViewset, ConfirmFileUpload, CandidateFiles,FileUpload, CandidateWithoutFullLocation,GetFilterData
from rest_framework.routers import DefaultRouter
from django.urls import path


router = DefaultRouter()
router.register(r'without-location', CandidateWithoutFullLocation, basename='candidate-location')
router.register(r'files', CandidateFiles, basename='files')
router.register(r'', CandidateViewset, basename='candidate')



urlpatterns = [
    path('confirm-file/', ConfirmFileUpload.as_view(), name='upload-file'),
    path('upload/', FileUpload.as_view(), name='upload-file'),
    path('get-filter-data', GetFilterData.as_view(), name='filter_data')
    
]

urlpatterns += router.urls