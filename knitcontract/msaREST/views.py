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
from contract.models import ContractStatus
from datetime import datetime
from msa.forms import validate_document
from random import randint, randrange
from . serializers import MSAListSerializer, MSASerializer
from django.shortcuts import get_object_or_404

class ContractPagination(PageNumberPagination):
    page_size = 2  # Number of records per page

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
        return Response({'message': 'Master agreement saved successfully.'}, status=rest_status.HTTP_201_CREATED)
    

class MSAList(APIView):
    def get(self, request, format=None):
        msas = MSA.objects.all()
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
            serializer.save()
            return Response({'success': True, 'message': 'Form updated successfully!'}, status=rest_status.HTTP_200_OK)
        else:
            return Response({'success': False, 'errors': serializer.errors}, status=rest_status.HTTP_400_BAD_REQUEST)
    

