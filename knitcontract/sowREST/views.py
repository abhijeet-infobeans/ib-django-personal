from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework import status as rest_status
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from .serializers import SOWSerializer
from sow.models import SOW
from rest_framework.pagination import PageNumberPagination
from .serializers import SOWListSerializer
from rest_framework.parsers import FormParser, MultiPartParser
from django.shortcuts import get_object_or_404
from contract.models import ContractStatus, DocumentRevision
from document_approval.models import DocumentApproval
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
import json

class ContractPagination(PageNumberPagination):
    page_size = 2  # Number of records per page
   
def getActionItemsByGroup(id, group=''):
        # get group ID by Name
        match group:
            case 'Client':
                status_id = ContractStatus.objects.values_list('id', flat=True).filter(status='Awaiting Client Signature')
                result = SOW.objects.filter(client=id, status__in=status_id)
        return result
    
class SOWCreateAPIView(CreateAPIView):
    queryset = SOW.objects.all()
    serializer_class = SOWSerializer
    # In CreateAPIView from Django Rest Framework (DRF) to create a new record, you can access the id of the newly created record by overriding the perform_create() method
    def perform_create(self, serializer):
        # Save the new instance, and get the newly created record
        new_instance = serializer.save()
        # Access the ID of the new instance
        new_sow_id = new_instance.id
        new_sow_doc_path = new_instance.sow_doc_path
        new_created_by = new_instance.created_by.id
        
        # Add entry in Revision table
        content_type = ContentType.objects.get_for_model(SOW)
        new_rev_num = 1
        revision_obj = DocumentRevision.objects.create(
            revision_number = new_rev_num,
            object_id = new_sow_id,
            file_path = new_sow_doc_path,
            comment = 'System generated',
            content_type_id = content_type.id,
            revision_by_id = new_created_by
        )
        SOW.objects.filter(pk=new_sow_id).update(current_revision_id=revision_obj.id)
    
class SOWList(APIView):
    def get(self, request, format=None):
        msas = SOW.objects.all().order_by('-id')
        client = request.GET.get('fc')
        status = request.GET.get('fs')
        search_query = request.GET.get('sq')
        
        if search_query:
            msas = msas.filter(
                Q(project_name__icontains=search_query)
                )
        
        # Apply filters dynamically
        if client:
            msas = msas.filter(client__id__icontains=client)
        if status:
            msas = msas.filter(status__id__icontains=status)
        paginator = ContractPagination()
        paginated_msas = paginator.paginate_queryset(msas, request)
        serializer = SOWListSerializer(paginated_msas, many=True)
        return paginator.get_paginated_response(serializer.data)
    
class SOWEditView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    
    def put(self, request, pk):
        sow_obj = get_object_or_404(SOW, pk=pk)
        serializer = SOWSerializer(sow_obj, data=request.data, partial=True)
        if serializer.is_valid():
            updated_obj=serializer.save()
            # check if file got replaced with new file
            if request.data['sow_doc_path']:
                # Check if entry is present on revision table if not please add one
                content_type = ContentType.objects.get_for_model(SOW)
                last_revision = DocumentRevision.objects.filter(object_id = updated_obj.id, content_type_id = content_type).order_by('-created_at').values()[:1]
                
                new_rev_num = 1
                if last_revision:
                    new_rev_num = int(last_revision[0]['revision_number'])+1
                    
                revision_obj = DocumentRevision.objects.create(
                    revision_number = new_rev_num,
                    object_id = updated_obj.id,
                    file_path = updated_obj.sow_doc_path,
                    comment = 'System generated',
                    content_type_id = content_type.id,
                    revision_by_id = updated_obj.created_by_id
                )
                SOW.objects.filter(pk=updated_obj.id).update(current_revision_id=revision_obj.id)
                
            return Response({'success': True, 'message': 'Form updated successfully!'}, status=rest_status.HTTP_200_OK)
        else:
            return Response({'success': False, 'errors': serializer.errors}, status=rest_status.HTTP_400_BAD_REQUEST)
        
class SOWGetActionables(APIView):
    def get(self, request, *args, **kwargs):
        # get user belogs to which group
        current_user_id = request.user.pk
        current_user_group = list(request.user.groups.values_list('name'))
        
        if (any('Client' in i for i in current_user_group)):
            actionable_records = getActionItemsByGroup(current_user_id, 'Client')
        
        serializer = SOWListSerializer(actionable_records, many=True)
        return Response(serializer.data)
    
class SOWStatusUpdate(APIView):
    def patch(self, request, *args, **kwargs):
        patch_data = request.data.dict()
        json_str = list(patch_data.keys())[0]
        parsed_data = json.loads(json_str)
        usp_i = parsed_data.get("usp_i")
        usp_a = parsed_data.get("usp_a")
        actionable_records = SOW.objects.get(pk=usp_i)
        print(actionable_records)
        if (usp_a == "a"):
            actionable_records.status_id = ContractStatus.objects.values_list('id', flat=True).filter(status = "Fully Signed")
            actionable_records.save()
        return Response({'success': True, 'message': 'Form updated successfully!'}, status=rest_status.HTTP_200_OK)
        
    