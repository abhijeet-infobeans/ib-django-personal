
from rest_framework import serializers
from msa.models import MSA
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError


class MSAListSerializer(serializers.ModelSerializer):
    client = serializers.CharField(source='client.username')
    status = serializers.CharField(source='status.status')
    created_by = serializers.CharField(source='created_by.get_full_name')
    msa_doc_path = serializers.FileField()
    class Meta:
        model = MSA
        fields = "__all__"
        
class MSASerializer(serializers.ModelSerializer):
    msa_doc_path = serializers.FileField(required=False)
    class Meta:
        model = MSA
        fields = "__all__"
        
    def validate(self, data):
        """
        Override the validate method to skip file validation if no file is provided.
        """
        if self.instance:
            if not self.initial_data.get('msa_doc_path'):  # No new file provided
                data['msa_doc_path'] = self.instance.msa_doc_path  # Retain the existing file
                
        client = data['client']
        user = User.objects.filter(pk=client.id, groups__name='Client')
        
        if not user:
            raise ValidationError({'error': 'Please select valid client'})
        
        if self.instance.pk:
            msa_obj = MSA.objects.filter(client=client).exclude(pk=self.instance.pk)
            if msa_obj:
                raise ValidationError({'error': 'Master Agreements is already present for selected client'})
        
        return data
        
