from django import forms
from . models import Company

class CompanyForm(forms.ModelForm):
    
    class Meta:
        model = Company
        fields = ['company_name', 'company_address']
        labels = {
            'company_name': 'Company Name',
            'company_address': 'Company Address',
        }
        widgets = {
            'company_name':forms.TextInput(attrs={'class': 'form-control'}),
            'company_address':forms.Textarea(attrs={'class': 'form-control'})
        }
        
        error_messages = {
            'company_name': {
                'required': 'Company Name must not be empty',
            },
            'company_address': {
                'required': 'Company Address must not be empty',
            }
        }
