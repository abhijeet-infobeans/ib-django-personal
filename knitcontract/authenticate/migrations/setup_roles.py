from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType    
from django.db import migrations


def setup_roles(apps, schema_editor):
    # Create groups
    admin_group, created = Group.objects.get_or_create(name='Admin')
    finance_group, created = Group.objects.get_or_create(name='Finance')
    department_head_group, created = Group.objects.get_or_create(name='Department Heads')
    project_manager_group, created = Group.objects.get_or_create(name='Project Managers')
    project_lead_group, created = Group.objects.get_or_create(name='Project Leads')
    guest_group, created = Group.objects.get_or_create(name='Guest')
    client_group, created = Group.objects.get_or_create(name='Client')


class Migration(migrations.Migration):
    operations = [
        migrations.RunPython(setup_roles),
    ]