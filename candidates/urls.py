from .views import CandidateViewset, ConfirmFileUpload, FileUpload
from rest_framework.routers import DefaultRouter
from django.urls import path


router = DefaultRouter()
router.register(r'', CandidateViewset, basename='candidate')

urlpatterns = [
    path('confirm-file/', ConfirmFileUpload.as_view(), name='upload-file'),
    path('upload/', FileUpload.as_view(), name='upload-file')
    
]

urlpatterns += router.urls