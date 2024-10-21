from django.db import models
from django.contrib.auth.models import User
from contract.models import ContractStatus
from msa.models import MSA
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.contenttypes.models import ContentType
from auditlog.models import AuditLog
from django.utils import timezone
from contract.models import DocumentRevision

# Create your models here.
class SOWType(models.Model):
    """Model definition for SOWType."""

    # TODO: Define fields here
    sow_type_name = models.CharField(
        max_length=100,
        unique=True
    )

    class Meta:
        """Meta definition for SOWType."""

        verbose_name = 'SOWType'
        verbose_name_plural = 'SOWTypes'

    def __str__(self):
        """Unicode representation of SOWType."""
        return self.sow_type_name

class SOW(models.Model):
    
    class InvoiceFrequency(models.TextChoices):
        Monthly = 'monthly',
        Fortnightly = 'fortnightly',

    project_name = models.CharField(
        max_length=255,
        unique=True,
    )
    msa = models.ForeignKey(MSA, on_delete=models.CASCADE, null=False)
    client = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='client_for_sow', limit_choices_to={'groups__name': 'Client'})
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='creator_for_sow')
    created_at = models.DateField(auto_now_add=True)
    sow_type = models.ForeignKey(SOWType, on_delete=models.CASCADE, null=False)
    status = models.ForeignKey(ContractStatus, on_delete=models.SET_NULL, null=True)
    duration = models.DurationField()
    start_date = models.DateField()
    end_date = models.DateField()
    project_cost = models.DecimalField(max_digits=12, decimal_places=3)
    currency = models.CharField(max_length=4)
    invoice_frequency = models.CharField(
        max_length=100,
        choices=InvoiceFrequency.choices,
        default=InvoiceFrequency.Monthly,
    )
    next_due_renewal = models.DateField()
    sow_doc_path = models.FileField(upload_to='sow_docs', null=False)
    current_revision = models.ForeignKey(DocumentRevision, on_delete=models.SET_NULL, null=True)
    

    class Meta:
        verbose_name = "SOW"
        verbose_name_plural = 'SOWs'

    def __str__(self):
        return f'{self.msa.msa_unq_no} - {self.project_name} - {self.sow_type.sow_type_name}'


@receiver(post_save, sender=SOW)
def log_sow_activity(sender, instance, created, **kwargs):
    content_type = ContentType.objects.get_for_model(instance)
    if created:
        action = 'Created'
        log_message = f"A new sow {instance.project_name} was created for client {instance.client.username} with MSA {instance.msa.msa_unq_no}."
    else:
        action = 'Updated'
        log_message = f"Contract  {instance.project_name} for client {instance.client.username} with MSA {instance.msa.msa_unq_no} was updated."

    # Create a log entry for this action
    AuditLog.objects.create(
        content_type=content_type,
        object_id=instance.id,
        action=action,
        log_message=log_message,
        timestamp=timezone.now()
    )