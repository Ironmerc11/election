
import os

import pandas as pd
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from users.permissions import IsAdminOrSuperUser

from .filters import CandidateFilter
from .models import Candidate, CandidateFile
from .serializers import CandidateSerializer,CandidateFileSerializer, FileUploadSerializer, CandidateWithoutLocationSerializer
from .tasks import add_candidates_to_db


class CandidateViewset(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'
    filterset_class = CandidateFilter
    
    # With cookie: cache requested url for each user for 2 hours
    @method_decorator(cache_page(60*60*5))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
  

class CandidateWithoutFullLocation(CandidateViewset):
    serializer_class = CandidateWithoutLocationSerializer
  

class ConfirmFileUpload(generics.CreateAPIView):
    serializer_class = FileUploadSerializer
    permission_classes = [IsAdminOrSuperUser]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data['file']
        _, file_extension = os.path.splitext(file.name)
        if file_extension == '.xlsx':   
            reader = pd.read_excel(file)
        elif file_extension == '.csv':
            reader = pd.read_csv(file)
        headers = ["STATE", "STATECODE", "SENATORIAL DISTRICT", "FEDERAL CONSTITUENCY",	"STATE CONSTITUENCY", "LGA", "LGACODE", "WARD", "WARDCODE", "POLLING UNIT", "PUCODE", "POSITION"]
        for _, row in reader.iterrows():
            for m in headers:
                if m in row:
                    pass
                else:
                    return Response({"error": f"The File is missing one header, the headers should be in this order {headers}"}, status.HTTP_400_BAD_REQUEST)
            
        return Response({"data": "None"},
                        status.HTTP_200_OK)
        


class FileUpload(generics.CreateAPIView):
    serializer_class = FileUploadSerializer
    permission_classes = [IsAdminOrSuperUser]
    
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data['file']
        year = serializer.validated_data.get('year', None)
        if not year:
            return Response({"error": f"Kindly input year"}, status.HTTP_400_BAD_REQUEST)
            
        _, file_extension = os.path.splitext(file.name)
        if file_extension == '.xlsx':   
            reader = pd.read_excel(file)
        elif file_extension == '.csv':
            reader = pd.read_csv(file)
        headers = ["STATE", "STATECODE", "SENATORIAL DISTRICT", "FEDERAL CONSTITUENCY",	"STATE CONSTITUENCY", "LGA", "LGACODE", "WARD", "WARDCODE", "POLLING UNIT", "PUCODE", "POSITION"]
        column_headers = reader.columns.ravel()
        parties = [item for item in column_headers[1:] if item not in headers]
        for _, row in reader.iterrows():
            for m in headers:
                if m in row:
                    pass
                else:
                    return Response({"error": f"The File is missing one header, the headers should be in this order {headers}"}, status.HTTP_400_BAD_REQUEST)
        
        saved_file = CandidateFile.objects.create(file=file)
        saved_file.status = 'Uploading'
        saved_file.save()
        add_candidates_to_db.delay(saved_file.id, parties, year)
            
        return Response({"message": "Upload successful, the data is being processed in the background"},
                        status.HTTP_200_OK)



class CandidateFiles(viewsets.ModelViewSet):
    queryset = CandidateFile.objects.all()
    serializer_class = CandidateFileSerializer
    