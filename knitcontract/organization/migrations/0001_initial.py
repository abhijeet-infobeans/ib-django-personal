# Generated by Django 4.2 on 2024-09-27 12:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organization_name', models.CharField(max_length=255, unique=True)),
                ('organization_address', models.TimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user_id', models.IntegerField(verbose_name=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL))),
            ],
        ),
    ]
