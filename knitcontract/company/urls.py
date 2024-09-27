from django.urls import path
from . import views



urlpatterns = [
    path('', views.CompanyListView.as_view(), name='company-list'),
    path('add', views.CompanyCreateView.as_view(), name='company-add')
]
