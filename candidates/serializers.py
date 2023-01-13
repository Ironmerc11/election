from dataclasses import field
from pyexpat import model
from .models import Candidate, Location, RunningPosition, Position, CandidateFile,ImageUpload, Party
from rest_framework import serializers



class CandidateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Candidate
        fields = '__all__'
        # exclude = ['location']
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if rep['candidate_image']:
            rep['candidate_image'] = rep['candidate_image'][13:]
        # if rep['party_image']:
        #     rep['party_image'] = rep['party_image'][13:]
        rep["location"] = LocationSerializer(instance.location.all(), many=True).data
        rep['party'] = PartySerializer(instance.party).data
        rep["position"] = RunningPositionSerializer(instance.position.all(), many=True).data
        return rep


class CandidateWithoutLocationSerializer(CandidateSerializer):
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        del rep["location"]
        return rep
        
class LocationSerializer(serializers.ModelSerializer):
     
    class Meta:
        model = Location
        fields = '__all__'
        
        
class LocationIdSerializer(LocationSerializer):
    
    class Meta:
        model = Location
        fields = ['id']

class RunningPositionSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = RunningPosition
        fields = '__all__'
        
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["position"] = PositionSerializer(instance.position).data
        return rep
        
class PositionSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = Position
        fields = '__all__'


class CandidateFileSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = CandidateFile
        fields = '__all__'     
        

class FileUploadSerializer(serializers.Serializer):
    TYPE_CHOICES = [
        ('CandidateData','CD'),
        ('LocationData', 'LD'),
    ]
    file = serializers.FileField()
    year = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    type = serializers.ChoiceField(required=True, choices=TYPE_CHOICES)
    
    

class ImageUploadSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ImageUpload
        fields = '__all__'
        


class PartySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Party
        fields = '__all__'