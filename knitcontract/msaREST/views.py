from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status as rest_status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.pagination import PageNumberPagination
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from msa.models import MSA
from contract.models import ContractStatus, DocumentRevision
from document_approval.models import DocumentApproval
from datetime import datetime
from msa.forms import validate_document
from random import randint, randrange
from . serializers import MSAListSerializer, MSASerializer
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
import json
from django.db.models import Q

class ContractPagination(PageNumberPagination):
    page_size = 5  # Number of records per page

# id: Current loging user ID    
def getActionItemsByGroup(id, group=''):
        # get group ID by Name
        match group:
            case 'Client':
                status_id = ContractStatus.objects.values_list('id', flat=True).filter(status='Awaiting Client Signature')
                result = MSA.objects.filter(client=id, status__in=status_id)
            case _:
                result = None
        
        return result

class MSACreateView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        client = request.data.get('client')
        created_by = request.data.get('created_by')
        signing_authority = request.data.get('signing_authority')
        ib_signing_authority = request.data.get('ib_signing_authority')
        signing_date = request.data.get('signing_date')
        status = request.data.get('status')
        msa_doc_path = request.FILES.get('msa_doc_path')

        # Validate required fields
        if not all([client, created_by, signing_authority, ib_signing_authority, msa_doc_path, status]):
            return Response(
                {
                'error': 'All fields are required.'
                }, 
                status=rest_status.HTTP_400_BAD_REQUEST)
        try:
            # Validate client is an integer
            client = int(client)
            user = User.objects.filter(pk=client, groups__name='Client').exists()
        except ValueError:
            return Response({'error': 'Invalid Client.'}, status=rest_status.HTTP_400_BAD_REQUEST)

        try:
            # Validate signing_authority is an email
            validate_email(signing_authority)
        except ValidationError:
            return Response({'error': 'Client signing authority must be a valid email.'}, status=rest_status.HTTP_400_BAD_REQUEST)

        try:
            # Validate signing_date is a valid date
            signing_date = datetime.strptime(signing_date, '%Y-%m-%d').date()
        except ValueError:
            return Response({'error': 'signing_date must be in the format YYYY-MM-DD.'}, status=rest_status.HTTP_400_BAD_REQUEST)
        
        try:
            filesize = msa_doc_path.size
            megabyte_limit = 20.0
            if filesize > megabyte_limit*1024*1024:
                return Response({'error': 'Please upload document with correct size.'}, status=rest_status.HTTP_400_BAD_REQUEST)
            if not msa_doc_path.name.endswith('.pdf'):
                return Response({'error': 'Please upload document in pdf format.'}, status=rest_status.HTTP_400_BAD_REQUEST)
        except ValidationError:
            return Response({'error': 'Please upload document in correct formate and size.'}, status=rest_status.HTTP_400_BAD_REQUEST)

        
        client_user = User.objects.get(pk=client)
        creating_user = User.objects.get(pk=created_by)
        contract_status = ContractStatus.objects.get(pk=status)
        unique_id = "msa-"+str(randint(100, 999))+"-"+str(randrange(100, 1000))
        
        # Create the MSA object
        master_agreement = MSA(
            msa_unq_no=unique_id,
            client=client_user,
            created_by=creating_user,
            signing_authority=signing_authority,
            signing_date=signing_date,
            ib_signing_authority=ib_signing_authority,
            status=contract_status,
            msa_doc_path=msa_doc_path
        )
        master_agreement.save()
        master_agreement_obj = master_agreement
        
        # Add entry in Revision table
        content_type = ContentType.objects.get_for_model(MSA)
        new_rev_num = 1
        revision_obj = DocumentRevision.objects.create(
            revision_number = new_rev_num,
            object_id = master_agreement_obj.id,
            file_path = master_agreement_obj.msa_doc_path,
            comment = 'System generated',
            content_type_id = content_type.id,
            revision_by_id = master_agreement_obj.created_by_id
        )
        MSA.objects.filter(pk=master_agreement_obj.id).update(current_revision_id=revision_obj.id)
        
        return Response({'message': 'Master agreement saved successfully.'}, status=rest_status.HTTP_201_CREATED)
    

class MSAList(APIView):
    def get(self, request, format=None):
        msas = MSA.objects.all().order_by('-id')
        # Get filter parameters from the request
        client = request.GET.get('fc')
        status = request.GET.get('fs')
        search_query = request.GET.get('sq')
        
        if search_query:
            msas = msas.filter(Q(msa_unq_no__icontains=search_query))
        
        # Apply filters dynamically
        if client:
            msas = msas.filter(client__id__icontains=client)
        if status:
            msas = msas.filter(status__id__icontains=status)
        
        paginator = ContractPagination()
        paginated_msas = paginator.paginate_queryset(msas, request)
        serializer = MSAListSerializer(paginated_msas, many=True)
        return paginator.get_paginated_response(serializer.data)
    
class MSAGetSingleDetail(RetrieveAPIView):
    queryset = MSA.objects.all()
    serializer_class = MSASerializer
    
class MSAEditView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    
    def put(self, request, pk):
        msa_obj = get_object_or_404(MSA, pk=pk)
        serializer = MSASerializer(msa_obj, data=request.data, partial=True)
        
        if serializer.is_valid():
            updated_obj = serializer.save()
            # check if file got replaced with new file
            if request.data['msa_doc_path']:
                # Check if entry is present on revision table if not please add one
                content_type = ContentType.objects.get_for_model(MSA)
                last_revision = DocumentRevision.objects.filter(object_id = updated_obj.id, content_type_id = content_type).order_by('-created_at').values()[:1]
                
                new_rev_num = 1
                if last_revision:
                    new_rev_num = int(last_revision[0]['revision_number'])+1
                    
                revision_obj = DocumentRevision.objects.create(
                    revision_number = new_rev_num,
                    object_id = updated_obj.id,
                    file_path = updated_obj.msa_doc_path,
                    comment = 'System generated',
                    content_type_id = content_type.id,
                    revision_by_id = updated_obj.created_by_id
                )
                MSA.objects.filter(pk=updated_obj.id).update(current_revision_id=revision_obj.id)
                
                            
            return Response({'success': True, 'message': 'Form updated successfully!'}, status=rest_status.HTTP_200_OK)
        else:
            return Response({'success': False, 'errors': serializer.errors}, status=rest_status.HTTP_400_BAD_REQUEST)
        
        
class MSAGetActionables(APIView):
     
    def get(self, request, *args, **kwargs):
        # get user belogs to which group
        current_user_id = request.user.pk
        current_user_group = list(request.user.groups.values_list('name'))
        
        if (any('Client' in i for i in current_user_group)):
            actionable_records = getActionItemsByGroup(current_user_id, 'Client')
        
        #actionable_records = 
        serializer = MSAListSerializer(actionable_records, many=True)
        return Response(serializer.data)
    
class MSAStatusUpdate(APIView):
    def patch(self, request, *args, **kwargs):
        patch_data = request.data.dict()
        json_str = list(patch_data.keys())[0]
        parsed_data = json.loads(json_str)
        usp_i = parsed_data.get("usp_i")
        usp_a = parsed_data.get("usp_a")
        actionable_records = MSA.objects.get(pk=usp_i)
        if (usp_a == "a"):
            actionable_records.status_id = ContractStatus.objects.values_list('id', flat=True).filter(status = "Fully Signed")
            actionable_records.save()
        return Response({'success': True, 'message': 'Form updated successfully!'}, status=rest_status.HTTP_200_OK)
        