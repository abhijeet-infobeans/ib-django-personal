# Generated by Django 4.2 on 2024-10-08 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sow', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sowtype',
            name='sow_type_name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]