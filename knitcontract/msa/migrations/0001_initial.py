# Generated by Django 4.2 on 2024-10-03 09:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contract', '0002_alter_contractstatus_options'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MSA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('msa_unq_no', models.CharField(max_length=100, unique=True)),
                ('signing_authority', models.EmailField(max_length=254)),
                ('signing_date', models.DateField()),
                ('ib_signing_authority', models.EmailField(max_length=254)),
                ('msa_doc_path', models.FileField(upload_to='msa_docs')),
                ('client_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='client', to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='creator', to=settings.AUTH_USER_MODEL)),
                ('status_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='contract.contractstatus')),
            ],
            options={
                'verbose_name': 'MSA',
                'verbose_name_plural': 'MSAs',
            },
        ),
    ]