# Generated by Django 4.2.15 on 2024-09-21 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0019_alter_patient_year_and_section'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='height',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name='patient',
            name='weight',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='patient',
            name='middle_name',
            field=models.CharField(default='N/A', max_length=100),
        ),
        migrations.AlterField(
            model_name='patient',
            name='suffix',
            field=models.CharField(blank=True, default='N/A', max_length=2),
            preserve_default=False,
        ),
    ]
