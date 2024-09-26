from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class DashboardView(LoginRequiredMixin,View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    def get(self, request, *args, **kwargs):
        return render(request, 'contract/dashboard.html')
