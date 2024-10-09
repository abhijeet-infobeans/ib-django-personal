from django import forms
from .models import MSA
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.utils.safestring import mark_safe

def validate_document(fieldfile_obj):
        filesize = fieldfile_obj.file.size
        megabyte_limit = 20.0
        if filesize > megabyte_limit*1024*1024:
            raise ValidationError("Max file size is %sMB" % str(megabyte_limit))
        
class MSAForm(forms.ModelForm):
    
    class Meta:
        model = MSA
        fields = ['id','client', 'signing_authority', 'signing_date', 'ib_signing_authority', 'status', 'msa_doc_path']
        labels = {
            'client': 'Client',
            'signing_authority': "Client's Signing Authority",
            'signing_date': 'Signing Date',
            'ib_signing_authority': 'IB Signing Authority',
            'status': 'Status',
            'msa_doc_path': 'Document'
        }
        widgets = {
            'client':forms.Select(attrs={'class': 'form-select'}),
            'signing_authority':forms.EmailInput(attrs={'class': 'form-control'}),
            'signing_date':forms.widgets.DateInput(
                attrs={
                    'type': 'date',
                    'placeholder': 'mm/dd/YYYY'
                },
                format=('%Y-%m-%d')
            ),
            'ib_signing_authority': forms.EmailInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'msa_doc_path': forms.FileField(
                allow_empty_file=False,
                validators=[FileExtensionValidator( ['pdf'] ), validate_document],
                help_text='Maximum file size allowed is 20MB'
            )
        }
        
        
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            group_name = 'Client'
            try:
                group = Group.objects.get(name=group_name)
                # Filter users by the specific group
                self.fields['client'].queryset = User.objects.filter(groups=group)
            except Group.DoesNotExist:
                self.fields['client'].queryset = User.objects.none()
                
            if self.instance and self.instance.pk:
                self.fields['msa_doc_path'].help_text = mark_safe(f'<a target="_blank" href="{self.instance.msa_doc_path.url}" title="{self.instance.msa_doc_path.name}" ><i class="bi bi-file-earmark-pdf"></i></a>')
                # If you want to make file upload optional during editing, you can remove the "required" attribute
                self.fields['msa_doc_path'].required = False
        
