import imp
from rest_framework import viewsets
from .models import Candidate
from .serializers import CandidateSerializer


class CandidateViewset(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer