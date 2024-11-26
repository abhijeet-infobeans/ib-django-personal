from django.urls import path
from . import views

urlpatterns = [
   path('get-all-contract-status', views.GetAllContractStatus.as_view(), name = 'api-get-all-contract-status'),
   path('get-all-client-users', views.GetAllClientUsers.as_view(), name = 'api-get-all-client-users')
]
