from django.db import models

class Patient_data(models.Model):
    student_number = models.CharField(max_length=10, primary_key=True)
    first_name = models.CharField(max_length=256)
    middle_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    suffix = models.CharField(max_length=256, blank=True)
    SEX_CHOICES = {
        "male": "Male",
        "female": "Female"
    }
    sex = models.CharField(max_length=256, choices=SEX_CHOICES)
    age = models.PositiveIntegerField(default=0)
    address = models.CharField(max_length=256)
    course = models.CharField(max_length=256, blank=True)
    year = models.PositiveIntegerField(blank=True, default=0)
    section = models.CharField(blank=True, max_length=1)


