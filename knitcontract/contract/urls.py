from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('myactionables', views.MyActionableView.as_view(), name='myactionables')
]
