
import collections
from datetime import datetime, timedelta
import os
from candidates.utils import flatten_array,array_to_dict
from django.utils.timezone import make_aware
import pandas as pd
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from users.permissions import IsAdminOrSuperUser
# import django_rq

from .filter_select_fields import get_filter_data
from .filters import CandidateFilter, LocationFilter
from .models import Candidate, CandidateFile, Location, SearchQuery, ImageUpload
from .serializers import (CandidateFileSerializer, CandidateSerializer,
                          CandidateWithoutLocationSerializer,
                          FileUploadSerializer, LocationSerializer,LocationIdSerializer, ImageUploadSerializer)
from .tasks import add_candidates_to_db, add_candidates_data_to_db, read_excel


class CandidateViewset(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'
    filterset_class = CandidateFilter
    ordering = ['id']

    
    # With cookie: cache requested url for each user for 2 hours
    @method_decorator(cache_page(60*60*5))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    # Used this method to hack the caching and also 
    def finalize_response(self, request, response, *args, **kwargs):
        query_params = dict(request.query_params)
        query_params.pop('page', None)
        filter_combo = ("+").join(list(query_params.keys()))
        if filter_combo:
            SearchQuery.objects.create(
                filter_combo = ("+").join(list(query_params.keys())),
                keywords = list(request.query_params.values())
            )
        return super().finalize_response(request, response, *args, **kwargs)
  

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
        # headers = ["STATE", "STATECODE", "SENATORIAL DISTRICT", "FEDERAL CONSTITUENCY",	"STATE CONSTITUENCY", "LGA", "LGACODE", "WARD", "WARDCODE", "POLLING UNIT", "PUCODE", "POSITION"]
        headers = ["STATE", "LGA", "WARD", "POLLING UNIT", "PUCODE", "POSITION"]
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
        type = serializer.validated_data['type']
 
            
        if not year:
            return Response({"error": f"Kindly input year"}, status.HTTP_400_BAD_REQUEST)
            
        _, file_extension = os.path.splitext(file.name)
        if file_extension == '.xlsx' or file_extension == '.xls':   
            reader = pd.read_excel(file, 'Sheet1')
        elif file_extension == '.csv':
            reader = pd.read_csv(file)
            
        if type == 'CandidateData':
            saved_file = CandidateFile.objects.create(file=file, year=year)
            saved_file.status = 'Uploading'
            saved_file.save()
            df = read_excel(path=saved_file.file.url, sheet_name='Sheet1')
            out = df.to_dict(orient='records')
            add_candidates_data_to_db.delay(saved_file.id, out)
            # django_rq.enqueue(add_candidates_data_to_db, saved_file.id, df)
            return Response({"message": "Upload successful, the data is being processed in the background"},
                        status.HTTP_200_OK)
            
        
        headers = ["STATE", "LGA", "WARD", "POLLING UNIT", "PUCODE", "POSITION"]
        column_headers = reader.columns.ravel()
        parties = [item for item in column_headers[1:] if item not in headers]
        for _, row in reader.iterrows():
            for m in headers:
                if m in row:
                    pass
                else:
                    return Response({"error": f"The File is missing one header, the headers should be in this order {headers}"}, status.HTTP_400_BAD_REQUEST)
        
        saved_file = CandidateFile.objects.create(file=file, year=year)
        saved_file.status = 'Uploading'
        saved_file.type = type
        saved_file.save()
        df = read_excel(path=saved_file.file.url, sheet_name='Sheet1')
        out = df.to_dict(orient='records')
        df_out = out[0:20]
        add_candidates_to_db.delay(saved_file.id, df_out, parties, year)
        # add_candidates_to_db.delay(saved_file.id, out, parties, year)
        return Response({"message": "Upload successful, the data is being processed in the background"},
                        status.HTTP_200_OK)

class CandidateFiles(viewsets.ModelViewSet):
    queryset = CandidateFile.objects.all()
    serializer_class = CandidateFileSerializer
    permission_classes = [IsAdminOrSuperUser]


class GetFilterData(views.APIView):
    
    def get(self, request, format=None):
        """
            Get filter data from the db
        """
        state = request.query_params.get('state')
        senatorial_district = request.query_params.get('senatorial_district')
        federal_constituency = request.query_params.get('federal_constituency')
        state_constituency = request.query_params.get('state_constituency')
        lga = request.query_params.get('lga')
        ward = request.query_params.get('ward')
        polling_unit = request.query_params.get('polling_unit')
        
        data = get_filter_data(request.query_params.get('filter'),state,senatorial_district,federal_constituency,
                               state_constituency, lga, ward, polling_unit)
        return Response(data)
    

class SearchQueryView(views.APIView):
    permission_classes = [IsAdminOrSuperUser]

    @method_decorator(cache_page(60*60*5))
    @method_decorator(vary_on_cookie)
    def get(self, request, format=None):
        period = request.query_params.get('period')
        enddate = make_aware(datetime.today())
        if period.lower() == 'day':
            startdate = enddate - timedelta(days=1)
        elif period.lower() == 'week':
            startdate = enddate - timedelta(days=7)
        elif period.lower() == 'month':
            startdate = enddate - timedelta(days=30)

        if period.lower() == 'lifetime':
            queries = SearchQuery.objects.all()
        else:
            queries = SearchQuery.objects.filter(created_at__range=[startdate, enddate])
            
    
        filters = queries.count()
        searches_today = flatten_array(list(queries.values_list('keywords', flat=True)))
        
        search_params_list = flatten_array(list(queries.values_list('keywords', flat=True)))
        filter_params_list = queries.values_list('filter_combo', flat=True) 
        
        filter_params = array_to_dict(collections.Counter(filter_params_list).most_common(10))

        search_params = array_to_dict(collections.Counter(search_params_list).most_common(10))
        res = {
            "keywords":search_params,
            "filters":filter_params,
            "total_filters":filters,
            "searches":len(searches_today)
        }
        return Response(res)

class LocationView(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    # permission_classes = [IsAdminOrSuperUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'
    filterset_class = LocationFilter
    
    @action(detail=False)
    def get_ids(self, request):
        # queryset = self.queryset
        # print(queryset)
        queryset = self.filter_queryset(self.get_queryset())
        serializer = LocationIdSerializer(queryset, many=True)
        final_data = []
        for m in serializer.data:
            final_data.append(m.get('id'))
        return Response(final_data)
    

class ImageUploadView(viewsets.ModelViewSet):
    queryset = ImageUpload.objects.all()
    serializer_class = ImageUploadSerializer
    permission_classes = [IsAdminOrSuperUser]
    
