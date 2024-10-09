from django.urls import path
from . import views



urlpatterns = [
    path('', views.OrganizationListView.as_view(), name='organization-list'),
    path('add', views.OrganizationCreateView.as_view(), name='organization-add'),
    path('edit/<int:pk>', views.OrganizationUpdateView.as_view(), name='organization-edit')
]
