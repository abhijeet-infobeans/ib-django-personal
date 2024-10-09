from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import FormView, UpdateView
from .forms import SOWForm
from django.urls import reverse_lazy
from . models import SOW

# Create your views here.

class SOWListView(TemplateView):
    model = SOW
    template_name = "sow/index.html"

class SOWCreateView(FormView):
    template_name = 'sow/add_sow.html'
    form_class = SOWForm
    success_url = reverse_lazy('sow-list')


class SOWEditView(UpdateView):
    model = SOW
    template_name = 'sow/edit_sow.html'
    form_class = SOWForm

