from django.contrib import admin
from . models import ContractStatus
from .models import DocumentRevision

# Register your models here.
admin.site.register(ContractStatus)
admin.site.register(DocumentRevision)