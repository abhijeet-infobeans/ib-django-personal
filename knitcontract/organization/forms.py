from django import forms
from . models import Organization

class OrganizationForm(forms.ModelForm):
    
    class Meta:
        model = Organization
        fields = ['organization_name', 'organization_address', 'organization_type']
        labels = {
            'organization_name': 'Organization Name',
            'organization_address': 'Organization Address',
            'organization_type': 'Organization Type'
        }
        widgets = {
            'organization_name':forms.TextInput(attrs={'class': 'form-control'}),
            'organization_address':forms.Textarea(attrs={'class': 'form-control'}),
            'organization_type':forms.Select(attrs={'class': 'form-select'})
            
            
        }
        
        error_messages = {
            'organization_name': {
                'required': 'Organization Name must not be empty',
            },
            'organization_address': {
                'required': 'Organization Address must not be empty',
            }
        }
