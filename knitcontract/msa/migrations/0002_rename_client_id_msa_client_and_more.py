# Generated by Django 4.2 on 2024-10-04 13:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('msa', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='msa',
            old_name='client_id',
            new_name='client',
        ),
        migrations.RenameField(
            model_name='msa',
            old_name='status_id',
            new_name='status',
        ),
    ]