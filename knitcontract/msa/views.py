from django.shortcuts import render
from django.views.generic.edit import CreateView,UpdateView
from django.views.generic import ListView
from django.contrib.auth.models import Group, User
from .models import MSA
from .forms import MSAForm

# Create your views here.

class MSACreateView(CreateView):
    model = MSA
    template_name = "msa/add_msa.html"
    form_class = MSAForm
    

class MSAListView(ListView):
    model = MSA
    template_name = "msa/index.html"
    
class MSAEditView(UpdateView):
    model = MSA
    template_name = "msa/edit_msa.html"
    form_class = MSAForm

    
