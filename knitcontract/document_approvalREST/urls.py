from django.urls import path
from . import views

urlpatterns = [
   path('assign/<str:doc_type>/<int:pk>', views.DocumentApprovalCreateAPIView.as_view(), name = 'api-assign-for-approval')
]
