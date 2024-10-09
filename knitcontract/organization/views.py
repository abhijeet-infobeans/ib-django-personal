from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView

from .forms import OrganizationForm
from .models import Organization

# Create your views here.
class OrganizationListView(ListView):
    model = Organization
    template_name = 'organization/index.html'
    context_object_name = 'organizations'

class OrganizationCreateView(CreateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'organization/add_organization.html'
    success_url = '/organization'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(OrganizationCreateView, self).form_valid(form)


class OrganizationUpdateView(UpdateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'organization/edit_organization.html'
    success_url = '/organization'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_value = self.object # as we are using DetailView and fetching details from Id Django is performing in backgroud
        context['pk'] =  selected_value.id
        return context

