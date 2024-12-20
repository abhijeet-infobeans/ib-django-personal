from django.urls import path
from . import views



urlpatterns = [
    path('add', views.MSACreateView.as_view(), name='api-msa-add'),
    path('', views.MSAList.as_view(), name='api-msa-list'),
    path('edit/<int:pk>', views.MSAEditView.as_view(), name='api-msa-edit'),
    path('getMSAactionables', views.MSAGetActionables.as_view(), name='api-msa-actionables'),
    path('mas-status-update', views.MSAStatusUpdate.as_view(), name='api-mas-status-update')
]
