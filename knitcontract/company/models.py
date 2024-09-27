from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Company(models.Model):
    company_name = models.CharField(
        max_length=255,
        unique=True,
        blank=False
    )
    company_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
