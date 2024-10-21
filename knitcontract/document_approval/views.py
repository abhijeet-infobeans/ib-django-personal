from django.shortcuts import render
from django.views.generic import CreateView
from .models import DocumentApproval
from .forms import DocumentApprovalForm
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

# Create your views here.

class DocumentApprovalCreateView(CreateView):
    model = DocumentApproval
    form_class = DocumentApprovalForm
    template_name = "document_approval/assign.html"
    #context_object_name = 'document_approval'
    
    # Use get_queryset() to get the instance of the model
    def get_queryset(self):
        document_id = self.kwargs.get('pk')
        content_type_id = ContentType.objects.get(model=self.kwargs['doc_type']).id
        return DocumentApproval.objects.filter(object_id=document_id, content_type_id=content_type_id)
    
    # Overriding get_form() to pre-select checkboxes
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        document_approvals = self.get_queryset()
        
        # Fetch already assigned users for the current document
        assigned_users = User.objects.filter(documentapproval__in=document_approvals)
        
        # Preselect the checkboxes with the assigned users
        form.fields['assigned_to'].initial = assigned_users.distinct()
        return form
