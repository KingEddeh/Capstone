# Generated by Django 4.2.15 on 2024-09-21 08:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0021_stock_received_alter_patient_middle_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stock',
            old_name='received',
            new_name='disposed',
        ),
    ]
