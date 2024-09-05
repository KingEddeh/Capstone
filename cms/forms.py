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
            'unique_number': s2forms.Select2Widget(attrs={'class': 'form-control'}),
            'purpose': forms.TextInput(attrs={'class': 'form-control'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'received': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class MedcertSelect2Widget(s2forms.ModelSelect2Widget):
    search_fields = [
        "unique_number",
        "first_name__icontains",
        "middle_name__icontains",
        "last_name__icontains",
        "suffix__icontains",
    ]