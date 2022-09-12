from .models import Candidate, Location, RunningPosition, Position
from rest_framework import serializers



class CandidateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Candidate
        fields = '__all__'
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        # rep["location"] = LocationSerializer(instance.location.all(), many=True).data
        rep["position"] = RunningPositionSerializer(instance.position.all(), many=True).data
        return rep
        
class LocationSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = Location
        fields = '__all__'
        

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
        
        

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    year = serializers.CharField(allow_blank=True, allow_null=True, required=False)