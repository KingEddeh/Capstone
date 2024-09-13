from django.forms import ModelForm
from django import forms
from .models import *
from django_select2 import forms as s2forms


class PatientForm(forms.ModelForm):
    class Meta:
        model = patient
        fields = '__all__'
        exclude = ('created_at',)
        widgets = {
            'unique_number': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'suffix': forms.TextInput(attrs={'class': 'form-control'}),
            'sex': forms.Select(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'course': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'section': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_number': forms.TextInput(attrs={'class': 'form-control'}),
            'personal_email': forms.EmailInput(attrs={'class': 'form-control'}),
        }



class MedcertForm(forms.ModelForm):
    class Meta:
        model = Medicalcertificate_logbook
        fields = '__all__'
        exclude = ('created_at', 'provider')
        widgets = {
            'unique_number': s2forms.Select2Widget(attrs={'class': 'form-select'}), 
            'purpose': forms.TextInput(attrs={'class': 'form-control'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'received': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }



class ReferralForm(forms.ModelForm):
    class Meta:
        model = Referral
        fields = '__all__'
        exclude = ('created_at', 'provider')
        widgets = {
            'unique_number': s2forms.Select2Widget(attrs={'class': 'form-select'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'referred_hospital': s2forms.Select2Widget(attrs={'class': 'form-select'}),
        }



class TreatmentForm(forms.ModelForm):
    class Meta:
        model = Treatment_logbook
        fields = '__all__'
        exclude = ('created_at', 'provider')
        widgets = {
            'unique_number': s2forms.Select2Widget(attrs={'class': 'form-select'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }



class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = '__all__'
        exclude = ('created_at', 'provider')
        widgets = {
            'brand_name': forms.TextInput(attrs={'class': 'form-control'}),
            'generic_name': forms.TextInput(attrs={'class': 'form-control'}),
            'dosage_form': forms.TextInput(attrs={'class': 'form-control'}),
            'dosage_strength': forms.TextInput(attrs={'class': 'form-control'}),
        }



class InventoryForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = '__all__'
        exclude = ('created_at', 'initial_stocks', 'current_stock', 'provider')
        widgets = {
            'medicine': s2forms.Select2Widget(attrs={'class': 'form-select'}),
            'stock_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'unit': s2forms.Select2Widget(attrs={'class': 'form-select'}),
            'quantity_per_unit': forms.NumberInput(attrs={'class': 'form-control'}),
            'expiration_date': forms.DateInput(attrs={'class': 'form-control'}),
        }



class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = '__all__'
        exclude = ('provider',)
        widgets = {
            'expiration_date': forms.DateInput(attrs={'class': 'form-control'}),
            'treatment_logbook': s2forms.Select2Widget(attrs={'class': 'form-select'}),
            'medicine': s2forms.Select2Widget(attrs={'class': 'form-select'}),
            'quantity_prescribed': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }