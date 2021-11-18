from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Patient(models.Model):
    user = models.ForeignKey(User, null=True,on_delete=models.CASCADE, related_name='patients')
    name = models.CharField(unique=True, max_length=100, verbose_name='نام بیمار')
    code = models.IntegerField(unique=True, null=True, blank=True)

    class Meta:
        verbose_name = 'بیمار'
        verbose_name_plural = 'بیماران'

    def __str__(self):
        return self.name
