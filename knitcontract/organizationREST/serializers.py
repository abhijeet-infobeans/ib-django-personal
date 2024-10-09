from rest_framework import serializers
from organization.models import Organization

class OrganizationSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.get_full_name')
    class Meta:
        model = Organization
        fields = "__all__"
        extra_kwargs = {
            'user': {'read_only': True},
            'created_at': {'read_only': True},
            'organization_type': {'read_only': True}
        }

class OrganizationEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ('organization_name', 'organization_address')
        
class OrganizationAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = "__all__"
 