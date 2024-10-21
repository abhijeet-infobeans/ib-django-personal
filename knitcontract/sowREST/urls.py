from django.urls import path
from . import views

urlpatterns = [
    path('add', views.SOWCreateAPIView.as_view(), name='api-sow-add'),
    path('', views.SOWList.as_view(), name='api-sow-list'),
    path('edit/<int:pk>', views.SOWEditView.as_view(), name='api-sow-edit'),
    path('getSOWactionables', views.SOWGetActionables.as_view(), name='api-sow-actionables')
]
