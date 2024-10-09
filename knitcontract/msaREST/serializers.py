
from rest_framework import serializers
from msa.models import MSA

class MSAListSerializer(serializers.ModelSerializer):
    client = serializers.CharField(source='client.get_full_name')
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
        return data

