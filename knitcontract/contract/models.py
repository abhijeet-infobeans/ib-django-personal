from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class ContractStatus(models.Model):
    status = models.CharField(max_length=255)
    class Meta:
        verbose_name_plural = "Contract Status"
    
    def __str__(self):
        return self.status
    
class DocumentRevision(models.Model):
    revision_number = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    file_path = models.CharField(max_length=1000)
    comment = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    revision_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        verbose_name_plural = "Document Revisions"
        
    def __str__(self):
        return f'{self.revision_number}'
