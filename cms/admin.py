from django.contrib import admin
from .models import Patient_data_student

class my_admin(admin.ModelAdmin):
    pass
admin.site.register(Patient_data_student, my_admin)