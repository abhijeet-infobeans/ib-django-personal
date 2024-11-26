from django.db import models
from django.contrib.auth.models import User
from contract.models import ContractStatus
from contract.models import DocumentRevision
from auditlog.models import AuditLog
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

# Create your models here.
class MSA(models.Model):
    msa_unq_no = models.CharField(
        max_length=100,
        unique=True,
        null=False
    )
    client = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='client')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='creator')
    signing_authority = models.EmailField(null=False)
    signing_date = models.DateField()
    ib_signing_authority = models.EmailField(null=False)
    status = models.ForeignKey(ContractStatus, on_delete=models.SET_NULL, null=True)
    msa_doc_path = models.FileField(upload_to='msa_docs', null=False)
    created_at = models.DateField(auto_now_add=True)
    current_revision = models.ForeignKey(DocumentRevision, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "MSA"
        verbose_name_plural = "MSAs"

    def __str__(self):
        return self.msa_unq_no
    
    
@receiver(post_save, sender=MSA)
def log_sow_activity(sender, instance, created, **kwargs):
    content_type = ContentType.objects.get_for_model(instance)
    if created:
        action = 'Created'
        log_message = f"A new Agreement {instance.id} was created for client {instance.client.username} with MSA {instance.msa.msa_unq_no}."
    else:
        action = 'Updated'
        log_message = f"Agreement  {instance.id} for client {instance.client.username} with MSA {instance.msa.msa_unq_no} was updated."

    # Create a log entry for this action
    AuditLog.objects.create(
        content_type=content_type,
        object_id=instance.id,
        action=action,
        log_message=log_message,
        timestamp=timezone.now()
    )


