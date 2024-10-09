from rest_framework import serializers
from .models import SOW

class SOWSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SOW
        fields = '__all__'