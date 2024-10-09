from django.db import models

# Create your models here.
class ContractStatus(models.Model):
    status = models.CharField(max_length=255)
    class Meta:
        verbose_name_plural = "Contract Status"
    
    def __str__(self):
        return self.status
