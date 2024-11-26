from rest_framework import serializers
from sow.models import SOW

class SOWListSerializer(serializers.ModelSerializer):
    client = serializers.CharField(source='client.get_full_name')
    msa = serializers.CharField(source='msa.msa_unq_no')
    sow_type = serializers.CharField(source='sow_type.sow_type_name')
    status = serializers.CharField(source='status.status')
    created_by = serializers.CharField(source='created_by.get_full_name')
    sow_doc_path = serializers.FileField()
    client_uname = serializers.CharField(source='client.username')
    
    class Meta:
        model = SOW
        fields = "__all__"
        
class SOWSerializer(serializers.ModelSerializer):
    sow_doc_path = serializers.FileField(required=False)
    class Meta:
        model = SOW
        fields = "__all__"
        
    def validate(self, data):
        """
        Override the validate method to skip file validation if no file is provided.
        """
        if self.instance:
            if not self.initial_data.get('sow_doc_path'):  # No new file provided
                data['sow_doc_path'] = self.instance.sow_doc_path  # Retain the existing file
        return data