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

class ContractPagination(PageNumberPagination):
    page_size = 2  # Number of records per page
    
    
class SOWCreateAPIView(CreateAPIView):
    queryset = SOW.objects.all()
    serializer_class = SOWSerializer
    
class SOWList(APIView):
    def get(self, request, format=None):
        msas = SOW.objects.all()
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
            serializer.save()
            return Response({'success': True, 'message': 'Form updated successfully!'}, status=rest_status.HTTP_200_OK)
        else:
            return Response({'success': False, 'errors': serializer.errors}, status=rest_status.HTTP_400_BAD_REQUEST)
        
    