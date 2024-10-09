from django import forms
from .models import SOW, SOWType
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.utils.safestring import mark_safe

def validate_document(fieldfile_obj):
        filesize = fieldfile_obj.file.size
        megabyte_limit = 20.0
        if filesize > megabyte_limit*1024*1024:
            raise ValidationError("Max file size is %sMB" % str(megabyte_limit))
        
        
class SOWForm(forms.ModelForm):
    
    class Meta:
        model = SOW
        fields = ['project_name', 'msa', 'client', 'sow_type', 'status', 'duration', 'start_date', 'end_date',
                  'project_cost', 'currency', 'invoice_frequency', 'next_due_renewal', 'sow_doc_path']
        labels = {
            'sow_doc_path': 'Document'
        }
        widgets = {
            'project_name': forms.TextInput(attrs={'class': 'form-control'}),
            'msa': forms.Select(attrs={'class': 'form-select'}),
            'client':forms.Select(attrs={'class': 'form-select'}),
            'sow_type': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'duration': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.widgets.DateInput(
                attrs={
                    'type': 'date',
                    'placeholder': 'mm/dd/YYYY'
                },
                format=('%Y-%m-%d')
            ),
            'end_date': forms.widgets.DateInput(
                attrs={
                    'type': 'date',
                    'placeholder': 'mm/dd/YYYY'
                },
                format=('%Y-%m-%d')
            ),
            'project_cost': forms.TextInput(attrs={'class': 'form-control'}),
            'currency': forms.TextInput(attrs={'class': 'form-control'}),
            'invoice_frequency': forms.Select(attrs={'class': 'form-select'}),
            'next_due_renewal': forms.widgets.DateInput(
                attrs={
                    'type': 'date',
                    'placeholder': 'mm/dd/YYYY'
                },
                format=('%Y-%m-%d')
            ),
            'sow_doc_path': forms.FileField(
                allow_empty_file=False,
                validators=[FileExtensionValidator( ['pdf'] ), validate_document],
                help_text='Maximum file size allowed is 20MB'
            )
            
        }
    
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if self.instance and self.instance.pk:
                self.fields['sow_doc_path'].help_text = mark_safe(f'<a target="_blank" href="{self.instance.sow_doc_path.url}" title="{self.instance.sow_doc_path.name}" ><i class="bi bi-file-earmark-pdf"></i></a>')
                # If you want to make file upload optional during editing, you can remove the "required" attribute
                self.fields['sow_doc_path'].required = False
