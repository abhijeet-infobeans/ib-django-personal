from django.db import models
from django.contrib.auth.models import User
from contract.models import ContractStatus

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

    class Meta:
        verbose_name = "MSA"
        verbose_name_plural = "MSAs"

    def __str__(self):
        return self.msa_unq_no


