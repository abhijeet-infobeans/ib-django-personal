from django.urls import path
from . import views


urlpatterns = [
    path('add', views.MSACreateView.as_view(), name='msa-add'),
    path('', views.MSAListView.as_view(), name='msa-list'),
    path('edit/<int:pk>', views.MSAEditView.as_view(), name='msa-edit')
]
