# Generated by Django 4.2.15 on 2024-09-18 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0012_remove_patient_age_patient_birthday'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='provider',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='patient',
            name='provider_updated',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
