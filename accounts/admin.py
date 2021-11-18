from django.contrib import admin
from .models import Patient


# Register your models here.
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    fields = ['name', 'user']
