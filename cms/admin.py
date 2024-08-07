from django.contrib import admin
from .models import Patient_data_student

class Patient_data_admin(admin.ModelAdmin):
    pass
admin.site.register(Patient_data_student, Patient_data_admin)