from django.db import models
from django.utils import timezone

"""
to do:
1. ayusin yung max length
2. add data validation
3. double check relationships
4. add audit trail shits
"""

class AutoDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        return timezone.now()

#primary keys
class Patient_data_student(models.Model):
    created_at = models.DateField(default=timezone.now)
    student_number = models.CharField(max_length=10)
    first_name = models.CharField(max_length=256)
    middle_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    suffix = models.CharField(max_length=256, blank=True)
    SEX_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
    ]
    sex = models.CharField(max_length=256, choices=SEX_CHOICES)
    age = models.PositiveIntegerField(default=0)
    address = models.CharField(max_length=256)
    course = models.CharField(max_length=256, blank=True)
    year = models.PositiveIntegerField(blank=True, default=0)
    section = models.CharField(blank=True, max_length=1)
#mga wala sa documentation
    contact_number = models.PositiveIntegerField(default=0)
    emergency_number = models.PositiveIntegerField(default=0)
    personal_email = models.CharField(max_length=256)

class Healthcare_provider(models.Model):
    created_at = models.DateField(default=timezone.now)
    full_name = models.CharField(max_length=256)
    #removed job title, i think di na necessary
    contact_number = models.PositiveIntegerField(default=0)
    emergency_number = models.PositiveIntegerField(default=0)
    personal_email = models.CharField(max_length=256)

class Medicine(models.Model):
    created_at = models.DateField(default=timezone.now)
    brand_name = models.CharField(max_length=256)
    generic_name = models.CharField(max_length=256)
    dosage_form = models.CharField(max_length=256)
    dosage_strength = models.CharField(max_length=256)

class Inventory(models.Model):
    #medicine ID
    unit = models.CharField(max_length=256)
    expiration_date = models.DateField()
    inital_stocks = models.PositiveIntegerField(default=0)
    current_stock = models.PositiveIntegerField(default=0)

class Prescription(models.Model):
    pass#walang created at date kasi nasa treatment logbook ang date

#logbooks
class Medicalcertificate_logbook(models.Model):
    created_at = models.DateField(default=timezone.now) #datetime
    student_number = models.CharField(max_length=10) #idk if gagawin same number field for student and employee or seperate fields
    purpose = models.CharField(max_length=256)
    remarks = models.CharField(max_length=256)
    received = models.CharField(max_length=256)
    #lagay dito provider ID

class Treatment_logbook(models.Model):
    created_at = models.DateField(default=timezone.now)
    student_number = models.CharField(max_length=10)
    description = models.CharField(max_length=512)
    #prescription ID pk
    #provider_ID fk

class Referral(models.Model):
    created_at = models.DateField(default=timezone.now)
    #student_number
    description = models.CharField(max_length=512)
    #prescription ID fk
    referred_hospital = models.CharField(max_length=256)
    #provider ID fk




