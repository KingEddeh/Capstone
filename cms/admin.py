from django.contrib import admin
from .models import Patient_data

class Patient_data_admin(admin.ModelAdmin):
    pass
admin.site.register(Patient_data, Patient_data_admin)