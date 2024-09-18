from django.db import models
from django.utils import timezone


class patient(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    unique_number = models.CharField(unique=True, max_length=10)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    suffix = models.CharField(max_length=2, blank=True, null=True)
    SEX_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
    ]
    sex = models.CharField(max_length=6, choices=SEX_CHOICES)
    birthday = models.DateField(null=True)
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    brand_name = models.CharField(max_length=100)
    generic_name = models.CharField(max_length=100)
    dosage_form = models.CharField(max_length=100)
    dosage_strength = models.CharField(max_length=100)
    provider = models.CharField(max_length=100, blank=True, null=True)
    provider_updated = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        if self.provider == None:
            self.provider = self.user.username
        if self.provider_updated:
            self.provider_updated = self.user.username
        return super().save(*args, **kwargs)

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

    def save(self, *args, **kwargs):
        if self.provider == None:
            self.provider = self.user.username
        if self.pk == None:
            self.initial_stocks = self.stock_quantity * self.quantity_per_unit
            self.current_stock = self.initial_stocks
        if self.pk:
            consumed = self.initial_stocks - self.current_stock
            self.initial_stocks = self.stock_quantity * self.quantity_per_unit
            self.current_stock = self.initial_stocks - consumed
        if self.provider_updated:
            self.provider_updated = self.user.username
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.medicine.brand_name} {self.medicine.dosage_strength} Stock #{self.id}'



#logbooks
class Medicalcertificate_logbook(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    unique_number = models.ForeignKey('Patient', on_delete=models.RESTRICT)
    purpose = models.CharField(max_length=100)
    note = models.CharField(max_length=1000, null=True, blank=True)
    received = models.BooleanField()
    provider = models.CharField(max_length=100, blank=True)
    provider_updated = models.CharField(max_length=100, blank=True)
    
    def save(self, *args, **kwargs):
        if self.provider == None:
            self.provider = self.user.username
            self.provider_updated = self.user.username
        if self.provider_updated:
            self.provider_updated = self.user.username
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'Medical Certificate to {self.unique_number} by {self.provider}'



class Treatment_logbook(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    unique_number = models.ForeignKey('Patient', on_delete=models.RESTRICT)
    description = models.CharField(max_length=1000)
    provider = models.CharField(max_length=100)
    provider_updated = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        if self.provider == None:
            self.provider = self.user.username
            self.provider_updated = self.user.username
        if self.provider_updated:
            self.provider_updated = self.user.username
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'Treatment {self.unique_number} by {self.provider}'



class Referral(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    unique_number = models.ForeignKey('Patient', on_delete=models.RESTRICT)
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

    def save(self, *args, **kwargs):
        if self.provider == None:
            self.provider = self.user.username
            self.provider_updated = self.user.username
        if self.provider_updated:
            self.provider_updated = self.user.username
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'Referral {self.unique_number} by {self.provider}'



#for treatment logbook
class Prescription(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    treatment_logbook = models.ForeignKey('Treatment_logbook', on_delete=models.CASCADE, related_name='prescriptions')
    medicine = models.ForeignKey('Stock', on_delete=models.RESTRICT)
    quantity_prescribed = models.PositiveIntegerField(default=1)
    description = models.CharField(max_length=1000, null=True, blank=True)
    provider = models.CharField(max_length=100, blank=True)
    provider_updated = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        if self.provider == None:
            self.provider = self.user.username
            self.provider_updated = self.user.username
        if self.medicine.current_stock >= self.quantity_prescribed:
            self.medicine.current_stock -= self.quantity_prescribed
            self.medicine.save()
        else:
            raise ValueError(f"Not enough stock for {self.medicine.medicine.brand_name}")
        if self.provider_updated:
            self.provider_updated = self.user.username
        return super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        if self.medicine:
            self.medicine.current_stock += self.quantity_prescribed
            self.medicine.save()
        return super().delete(*args, **kwargs)

    def __str__(self):
        return f'{self.quantity_prescribed} {self.medicine}'