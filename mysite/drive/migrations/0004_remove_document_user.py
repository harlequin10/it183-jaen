# Generated by Django 5.0 on 2024-12-07 12:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drive', '0003_alter_document_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='user',
        ),
    ]
