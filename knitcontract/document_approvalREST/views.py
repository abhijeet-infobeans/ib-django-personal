from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status as rest_status
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from document_approval.models import DocumentApproval
from django.contrib.contenttypes.models import ContentType

# Create your views here.
class DocumentApprovalCreateAPIView(CreateAPIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        users = request.data.get('assigned_to')
        created_by = request.data.get('created_by')
        users_list = users.split(",")

        # Validate required fields
        if not all([users, created_by]):
            return Response(
                {
                'error': 'All fields are required.'
                }, 
                status=rest_status.HTTP_400_BAD_REQUEST)
        
        try:
            # Validate client is an integer
            user = User.objects.filter(pk__in=users_list, groups__name='Client')
            if user:
                raise ValidationError({'error': 'Invalid User.'}, code=rest_status.HTTP_400_BAD_REQUEST)
        except ValidationError:
            return Response({'error': 'Invalid User.'}, status=rest_status.HTTP_400_BAD_REQUEST)
        content_type_id = ContentType.objects.get(model=self.kwargs['doc_type']).id
        # delete the list of existing assigned users
        existing_records = DocumentApproval.objects.filter(object_id = self.kwargs['pk'],content_type_id = content_type_id).values()
       
        extra_for_del = []
        if existing_records:
            for itm in existing_records:
                if str(itm['assigned_to_id']) not in users_list:
                    extra_for_del.append(itm['id'])
        
        for user in users_list:
            is_record_present = DocumentApproval.objects.filter(object_id = self.kwargs['pk'],assigned_to_id = user,content_type_id = content_type_id).exists()
            if not is_record_present:
                docApproval_obj = DocumentApproval(
                    object_id = self.kwargs['pk'],
                    assigned_to_id = user,
                    content_type_id = content_type_id
                )
                docApproval_obj.save()
        # Delete extra records
        if len(extra_for_del) > 0:
            for del_id in extra_for_del:
                DocumentApproval.objects.filter(pk=del_id).delete()
        
        return Response({'message': 'Approvers saved successfully.'}, status=rest_status.HTTP_201_CREATED)