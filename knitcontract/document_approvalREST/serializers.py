
from rest_framework import serializers
from document_approval.models import DocumentApproval
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from msa.models import MSA
from sow.models import SOW
from msaREST.serializers import MSAListSerializer
from sowREST.serializers import SOWListSerializer


class DocumentApprovalListSerializer(serializers.ModelSerializer):
    
    related_object = serializers.SerializerMethodField()
    
    class Meta:
        model = DocumentApproval
        fields = "__all__"
        
    def get_related_object(self, obj):
            # Get the model class based on the content_type
            model_class = obj.content_type.model_class()
            
            # Fetch the actual related object based on object_id
            related_object = model_class.objects.get(id=obj.object_id)
            print(related_object)
            # Dynamically choose the correct serializer for the related model
            if isinstance(related_object, MSA):
                return MSAListSerializer(related_object).data
            if isinstance(related_object, SOW):
                return SOWListSerializer(related_object).data
            
            # Add additional serializers for other models as needed
            
            return None  # If no related object is found