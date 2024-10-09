from django.urls import path
from . import views

urlpatterns = [
    path('', views.getData, name='api-organization-list'),
    path('edit/<int:pk>', views.editData, name='api-organization-edit'),
    path('add', views.addData, name='api-organization-add')
]
