from django import forms
from .models import DocumentApproval
from django.contrib.auth.models import User

class DocumentApprovalForm(forms.ModelForm):
    assigned_to = forms.ModelMultipleChoiceField(
        queryset=User.objects.all().exclude(groups__name='Client'),
        label='Select User/s',
        widget=forms.CheckboxSelectMultiple
    )
    class Meta:
        model = DocumentApproval
        fields = ('assigned_to',)