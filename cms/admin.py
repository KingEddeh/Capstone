from django.contrib import admin
from .models import *

class my_admin(admin.ModelAdmin):
    pass
admin.site.register(patient, my_admin)
admin.site.register(Medicine, my_admin)
admin.site.register(Stock, my_admin)
admin.site.register(Medicalcertificate_logbook, my_admin)
admin.site.register(Treatment_logbook, my_admin)
admin.site.register(Referral, my_admin)
admin.site.register(Prescription, my_admin)
