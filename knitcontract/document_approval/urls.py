from django.urls import path
from . import views

urlpatterns = [
   path('assign/<str:doc_type>/<int:pk>', views.DocumentApprovalCreateView.as_view(), name = 'assign-for-approval')
]
