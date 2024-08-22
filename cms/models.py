from django.db import models
from django.utils import timezone

"""
to do:
1. ayusin yung max length
2. add data validation
3. double check relationships, add foreign keys/many to many
4. add audit trail shits?
"""

class AutoDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        return timezone.now()

class patient(models.Model):
    created_at = models.DateField(default=timezone.now)
    unique_number = models.CharField(primary_key=True, max_length=10)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    suffix = models.CharField(max_length=100, blank=True, null=True)
    SEX_CHOICES = [
        ("m", "Male"),
        ("f", "Female"),
    ]
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    age = models.PositiveIntegerField(default=0)
    address = models.CharField(max_length=100)
    #for student only
    course = models.CharField(max_length=100, blank=True, null=True)
    year = models.PositiveIntegerField(blank=True, null=True)
    section = models.CharField(max_length=100, blank=True, null=True)
    #mga wala sa documentation
    contact_number = models.PositiveIntegerField(default=0)
    emergency_number = models.PositiveIntegerField(default=0)
    personal_email = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.unique_number} ({self.last_name}, {self.first_name})'

#healthcare provider model = authenticated user, gamit ng request.user

class Medicine(models.Model):
    created_at = models.DateField(default=timezone.now)
    brand_name = models.CharField(max_length=100)
    generic_name = models.CharField(max_length=100)
    dosage_form = models.CharField(max_length=100)
    dosage_strength = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.brand_name} ({self.generic_name})'


class Inventory(models.Model):
    medicine = models.ForeignKey("Medicine", on_delete=models.RESTRICT)
    unit = models.CharField(max_length=100)
    expiration_date = models.DateField()
    inital_stocks = models.PositiveIntegerField(default=0)
    current_stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'Stock no. {self.id} - {self.medicine.brand_name} - EXP: {self.expiration_date}'

#logbooks
class Medicalcertificate_logbook(models.Model):
    created_at = models.DateField(default=timezone.now) #datetime
    unique_number = models.ForeignKey('Patient', on_delete=models.RESTRICT)
    purpose = models.CharField(max_length=100)
    remarks = models.CharField(max_length=100)
    received = models.BooleanField()
    provider = models.CharField(max_length=100) #ilagay username ng logged in user sa views.py (username = request.user.username)
    def __str__(self):
        return f'{self.unique_number} ({self.unique_number.last_name}, {self.unique_number.first_name}) Medical Certificate'

class Treatment_logbook(models.Model):
    created_at = models.DateField(default=timezone.now)
    unique_number = models.ForeignKey('Patient', on_delete=models.RESTRICT)
    diagnosis = models.CharField(max_length=512, null=True, blank=True)
    provider = models.CharField(max_length=100)

class Referral(models.Model):
    created_at = models.DateField(default=timezone.now)
    unique_number = models.ForeignKey('Patient', on_delete=models.RESTRICT)
    diagnosis = models.CharField(max_length=512)
    treatment_logbook = models.ForeignKey('Treatment_logbook', on_delete=models.RESTRICT)
    referred_hospital = models.CharField(max_length=100)
    provider = models.CharField(max_length=100)

class Prescription(models.Model):
    treatment_logbook = models.ForeignKey('Treatment_logbook', on_delete=models.RESTRICT)
    medicine = models.ForeignKey('Medicine', on_delete=models.RESTRICT)
    quantity_prescribed = models.PositiveIntegerField(default=1)
    diagnosis = models.CharField(max_length=512, null=True, blank=True)

    def __str__(self):
        return f'{self.treatment_logbook.unique_number} was given {self.quantity_prescribed} {self.medicine}'



