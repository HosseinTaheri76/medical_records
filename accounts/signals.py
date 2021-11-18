from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Patient
from random import randint


@receiver(post_save, sender=Patient)
def set_patient_code(sender, instance, created, **kwargs):
    if created:
        while True:
            try:
                instance.code = randint(100000, 999999)
                instance.save()
                break
            except Exception:
                continue
