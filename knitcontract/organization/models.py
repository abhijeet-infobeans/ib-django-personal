from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Organization(models.Model):
    
    class organization_group(models.TextChoices):
        VENDER = "vender"
        ORGANIZATION = "organization"
        
    
    organization_name = models.CharField(
        max_length=255,
        unique=True,
        blank=False
    )
    organization_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    organization_type = models.CharField(
        max_length=100,
        choices=organization_group.choices,
        default=organization_group.ORGANIZATION
    )

    def __str__(self):
        return self.organization_name
    