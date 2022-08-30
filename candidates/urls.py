from .views import CandidateViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', CandidateViewset, basename='candidate')
urlpatterns = router.urls