from django.urls import path
from . import views

urlpatterns = [
    path('add', views.SOWCreateView.as_view(), name='sow-add'),
    path('', views.SOWListView.as_view(), name='sow-list'),
    path('edit/<int:pk>', views.SOWEditView.as_view(), name='sow-edit')
]
