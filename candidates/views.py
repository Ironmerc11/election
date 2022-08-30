import imp
from rest_framework import viewsets
from .models import Candidate
from .serializers import CandidateSerializer
from django_filters.rest_framework import DjangoFilterBackend


class CandidateViewset(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'