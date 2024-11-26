from rest_framework import serializers
from contract.models import ContractStatus
from django.contrib.auth.models import User

class ContractStatusSerializerList(serializers.ModelSerializer):
    #statustext = serializers.CharField(source='ContractStatus.status')
    class Meta:
        model = ContractStatus
        fields = ['id', 'status']
        
class ClientUserSerializerList(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id','username','get_full_name']
        
        
