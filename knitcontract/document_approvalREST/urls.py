from django.urls import path
from . import views

urlpatterns = [
   path('assign/<str:doc_type>/<int:pk>', views.DocumentApprovalCreateAPIView.as_view(), name = 'api-assign-for-approval'),
   path('get-doc-approval-actionables', views.DocumentApprovalGetActionables.as_view(), name='api-get-doc-approval'),
   path('get-sow-doc-approval-actionables', views.DocumentApprovalGetActionablesSOW.as_view(), name='api-get-sow-doc-approval'),
   path('msa-status-update', views.DocumentStatusUpdate.as_view(), name='api-msa-doc-update-status')
]
