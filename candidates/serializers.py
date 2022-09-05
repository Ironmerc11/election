from .models import Candidate, Location
from rest_framework import serializers



class CandidateSerializer(serializers.ModelSerializer):
    # state = serializers.ReadOnlyField(source='location.state')
    
    class Meta:
        model = Candidate
        fields = '__all__'
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["location"] = LocationSerializer(instance.location.all(), many=True).data
        return rep
        
class LocationSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = Location
        fields = '__all__'