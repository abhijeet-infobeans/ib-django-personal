from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class DocumentApproval(models.Model):
    
    class ApprovalStatus(models.TextChoices):
        Pending = 'pending',
        Approved = 'approved',
        Rejected = 'rejected'

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    assigned_at = models.DateTimeField(default=timezone.now)
    action_at =  models.DateTimeField(null=True)
    decision = models.CharField(
        max_length=100,
        choices=ApprovalStatus.choices,
        default=ApprovalStatus.Pending,
    )
    
    class Meta:
        verbose_name = "DocumentApproval"
        verbose_name_plural = "DocumentApprovals"
        unique_together = ('object_id', 'content_type', 'assigned_to')

    def __str__(self):
        return str(self.id)
