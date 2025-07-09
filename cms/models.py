from django.db import models
from django.utils import timezone

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import calendar
from datetime import date
from django.db.models import Sum


class patient(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    unique_number = models.CharField(unique=True, max_length=10)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    suffix = models.CharField(max_length=10, blank=True)
    SEX_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
    ]
    sex = models.CharField(max_length=6, choices=SEX_CHOICES)
    height = models.CharField(max_length=10, blank=True)
    weight = models.CharField(max_length=10, blank=True)
    address = models.CharField(max_length=100, blank=True)
    #for student only
    DEPARTMENT_CHOICES = [
        ("Empl", "Employee"),
        ("COE", "COE - College of Education"),
        ("CEA", "CEA - College of Architecture and Engineering"),
        ("CBS", "CBS - College of Business Studies"),
        ("CAS", "CAS - College of Arts and Science"),
        ("CSSP", "CSSP - College of Scial Science and Philosophy"),
        ("CCS", "CCS - College of Computing Studies"),
        ("CHTM", "CHTM - College of Hospitality and Tourism Management"),
        ("CIT", "CIT - College of Industrial Technology"),
        ("Law", "Law - School of Law"),
        ("GS", "GS - Graduate Studies"),
        ("SHS", "SHS - Senior High School"),
        ("LHS", "LHS - Laboratory High School"),
    ]
    department = models.CharField(max_length=4, choices=DEPARTMENT_CHOICES)
    course = models.CharField(max_length=100, blank=True, null=True)
    year_and_section = models.CharField(max_length=10, blank=True)
    #mga wala sa documentation
    contact_number = models.PositiveIntegerField(default='09')
    provider = models.CharField(max_length=100, blank=True)
    provider_updated = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.last_name}, {self.first_name} {self.middle_name}'

#healthcare provider model = authenticated user, gamit ng request.user

class Medicine(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    brand_name = models.CharField(max_length=100)
    generic_name = models.CharField(max_length=100)
    dosage_form = models.CharField(max_length=100)
    dosage_strength = models.CharField(max_length=100)
    provider = models.CharField(max_length=100, blank=True, null=True)
    provider_updated = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.brand_name} ({self.generic_name})'

class Stock(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    medicine = models.ForeignKey("Medicine", on_delete=models.RESTRICT)
    stock_quantity = models.PositiveIntegerField(default=0)
    choices = [
        ("box", "Box"),
        ("piece", "Piece"),
    ]
    unit = models.CharField(max_length=5, choices=choices)
    quantity_per_unit = models.PositiveIntegerField(default=1)
    expiration_date = models.DateField()
    initial_stocks = models.PositiveIntegerField(blank=True, null=True)
    current_stock = models.PositiveIntegerField(blank=True, null=True)
    provider = models.CharField(max_length=100, blank=True, null=True)
    provider_updated = models.CharField(max_length=100, blank=True)
    disposed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.pk == None:
            self.initial_stocks = self.stock_quantity * self.quantity_per_unit
            self.current_stock = self.initial_stocks
        if self.pk:
            consumed = self.initial_stocks - self.current_stock
            self.initial_stocks = self.stock_quantity * self.quantity_per_unit
            self.current_stock = self.initial_stocks - consumed
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.medicine.brand_name} Stock #{self.id}'

#logbooks
class Medicalcertificate_logbook(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    unique_number = models.CharField(max_length=100)
    purpose = models.CharField(max_length=100)
    note = models.CharField(max_length=1000, null=True, blank=True)
    received = models.BooleanField()
    provider = models.CharField(max_length=100, blank=True)
    provider_updated = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f'Medical Certificate to {self.unique_number} by {self.provider}'

class Treatment_logbook(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    unique_number = models.ForeignKey('Patient', on_delete=models.RESTRICT)
    CATEGORY_CHOICES = [
        ("A", "A. Alimentary System"),
        ("B", "B. Respiratory System"),
        ("C", "C. Musculo-Skeletal System"),
        ("D", "D. Integumentary System"),
        ("E", "E. Urinary System"),
        ("F", "F. Metabolic Endocrine System"),
        ("G", "G. Cardiovascular System"),
        ("H", "H. Eyes, Ears, Nose & Throat Disorders"),
        ("I", "I. Communicable Diseases"),
        ("J", "J. Blood Disorders"),
        ("K", "K. Neurological Disorders"),
        ("L", "L. OB-GYNE Cases"),
        ("M", "M. Dental Cases"),
        ("N", "N. Physical Examinations"),
        ("O", "O. Referrals"),
        ("P", "P. Follow-up Check-up"),
        ("Q", "Q. Others"),
    ]
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES)
    description = models.CharField(max_length=1000)
    provider = models.CharField(max_length=100)
    provider_updated = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'Treatment {self.unique_number} by {self.provider}'

class Referral(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    unique_number = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, null=True, blank=True)
    HOSPITAL_CHOICES = [
        ("The Medical City Clark", "The Medical City Clark"),
        ("Angeles University Foundation Medical Center", "Angeles University Foundation Medical Center"),
        ("Mother Teresa of Calcutta Medical Center", "Mother Teresa of Calcutta Medical Center"),
        ("Jose B. Lingad Memorial Regional Hospital", "Jose B. Lingad Memorial Regional Hospital"),
        ("San Fernandino Hospital", "San Fernandino Hospital"),
        ("Mt. Carmel Medical Center", "Mt. Carmel Medical Center"),
        ("Sacred Heart Medical Center", "Sacred Heart Medical Center"),
        ("Our Lady of Mt. Carmel Medical Center", "Our Lady of Mt. Carmel Medical Center"),
    ]
    referred_hospital = models.CharField(max_length=100, choices=HOSPITAL_CHOICES)
    provider = models.CharField(max_length=100, blank=True)
    provider_updated = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'Referral {self.unique_number} by {self.provider}'

#for treatment logbook
class Prescription(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    treatment_logbook = models.ForeignKey('Treatment_logbook', on_delete=models.RESTRICT, related_name='prescriptions')
    stock = models.ForeignKey('Stock', on_delete=models.RESTRICT)
    medicine = models.CharField(max_length=100, null=True, blank=True)
    quantity_prescribed = models.PositiveIntegerField()
    description = models.CharField(max_length=1000, null=True, blank=True)
    provider = models.CharField(max_length=100, blank=True)
    provider_updated = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        # Fetch the original quantity prescribed (if the object already exists)
        if self.pk:
            original_prescription = Prescription.objects.get(pk=self.pk)
            original_quantity = original_prescription.quantity_prescribed
            original_stock = original_prescription.stock
        else:
            original_quantity = None
            original_stock = None
        
        # Check if it's a new prescription
        if not self.pk:
            self.medicine = self.stock.medicine.brand_name
            # Ensure there's enough stock for the new prescription
            if self.stock.current_stock >= self.quantity_prescribed:
                self.stock.current_stock -= self.quantity_prescribed
                self.stock.save()
            else:
                raise ValueError(f"Not enough stock for {self.stock.medicine.brand_name}")
        
        # Handle updates
        else:
            # If the stock was changed, reverse the quantity from the original stock
            if original_stock != self.stock:
                original_stock.current_stock += original_quantity
                original_stock.save()

                if self.stock.current_stock >= self.quantity_prescribed:
                    self.stock.current_stock -= self.quantity_prescribed
                else:
                    raise ValueError(f"Not enough stock for {self.stock.medicine.brand_name}")
            else:
                # Adjust stock based on the difference between original and new quantity prescribed
                quantity_difference = self.quantity_prescribed - original_quantity
                if self.stock.current_stock >= quantity_difference:
                    self.stock.current_stock -= quantity_difference
                else:
                    raise ValueError(f"Not enough stock for {self.stock.medicine.brand_name}")
            
            self.stock.save()

        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.stock.current_stock += self.quantity_prescribed
        self.stock.save()
        return super().delete(*args, **kwargs)

    def __str__(self):
        return f'{self.quantity_prescribed} {self.stock}'