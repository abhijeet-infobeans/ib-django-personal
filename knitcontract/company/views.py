from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView

from .forms import CompanyForm
from .models import Company

# Create your views here.
class CompanyListView(ListView):
    model = Company
    template_name = 'company/index.html'
    context_object_name = 'companies'

class CompanyCreateView(CreateView):
    model = Company
    form_class = CompanyForm
    template_name = 'company/add_company.html'
    success_url = '/company'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CompanyCreateView, self).form_valid(form)
