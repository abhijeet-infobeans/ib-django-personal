from django.shortcuts import render
from rest_framework.views import APIView
from contract.models import ContractStatus
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status as rest_status
from contractREST.serializers import ContractStatusSerializerList, ClientUserSerializerList

# Create your views here.
class GetAllContractStatus(APIView):
     
    def get(self, request, *args, **kwargs):
        # get user belogs to which group
        contract_statuses = ContractStatus.objects.all()
        serializer = ContractStatusSerializerList(contract_statuses, many=True)
        return Response({'success': True, 'message': serializer.data}, status=rest_status.HTTP_200_OK)
    
class GetAllClientUsers(APIView):
     
    def get(self, request, *args, **kwargs):
        # get user belogs to which group
        contract_statuses = User.objects.filter(is_active = 1, groups__name='Client')
        serializer = ClientUserSerializerList(contract_statuses, many=True)
        return Response({'success': True, 'message': serializer.data}, status=rest_status.HTTP_200_OK)