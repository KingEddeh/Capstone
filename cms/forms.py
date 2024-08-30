from django.forms import ModelForm
from .models import *

class PatientForm(ModelForm):
    class Meta:
        model = patient
        fields = '__all__'
        exclude = ('created_at',)