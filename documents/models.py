from django.db import models
from django.db.models import Q, Max, Min
from accounts.models import Patient
from jalali_date import date2jalali
from datetime import date
from utils import jalali_to_gregorian
from .uploaders import test_document_uploader, other_doc_uploader, prescription_img_uploader
from .validators import validate_file_extension


class VisitManager(models.Manager):

    def get_future_visits(self):
        today = date.today()
        return self.get_queryset().filter(visit_date__gt=today)

    def search(self, doctor_name=None, reason=None, visit_date_from=None, visit_date_to=None, future=None):
        base_qs = self.get_future_visits() if future else self.get_queryset()
        if visit_date_from:
            visit_date_start = jalali_to_gregorian(visit_date_from)
        else:
            visit_date_start = self.aggregate(min_date=Min('visit_date'))['min_date']
        if visit_date_to:
            visit_date_end = jalali_to_gregorian(visit_date_to)
        else:
            visit_date_end = self.aggregate(max_date=Max('visit_date'))['max_date']
        lookup = Q(visit_date__gte=visit_date_start) & Q(visit_date__lte=visit_date_end)
        if doctor_name:
            lookup &= Q(doctor_name__contains=doctor_name)
        if reason:
            lookup &= Q(reason__contains=reason)
        return base_qs.filter(lookup)


class TestManager(models.Manager):
    def search(self, test_date_from=None, test_date_to=None):
        if test_date_from:
            test_date_start = jalali_to_gregorian(test_date_from)
        else:
            test_date_start = self.aggregate(min_date=Min('test_date'))['min_date']
        if test_date_to:
            test_date_end = jalali_to_gregorian(test_date_to)
        else:
            test_date_end = self.aggregate(max_date=Max('test_date'))['max_date']
        return self.get_queryset().filter(test_date__gte=test_date_start, test_date__lte=test_date_end)


class OtherDocsManager(models.Manager):
    def search(self, doc_type, title=None, doc_date_from=None, doc_date_to=None):
        base_qs = self.get_queryset().filter(doc_type__exact=doc_type)
        if doc_date_from:
            doc_date_start = jalali_to_gregorian(doc_date_from)
        else:
            doc_date_start = self.aggregate(min_date=Min('doc_date'))['min_date']
        if doc_date_to:
            doc_date_end = jalali_to_gregorian(doc_date_to)
        else:
            doc_date_end = self.aggregate(max_date=Max('doc_date'))['max_date']
        lookup = Q(doc_date__gte=doc_date_start) & Q(doc_date__lte=doc_date_end)
        if title:
            lookup &= Q(title__icontains=title)
        return base_qs.filter(lookup)


class Doctor(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='doctors')
    name = models.CharField(max_length=150, verbose_name='نام پزشک')
    file_no = models.IntegerField(null=True, blank=True, verbose_name='شماره پرنده')
    clinic_phone = models.CharField(max_length=11, null=True, blank=True, verbose_name='شماره مطب')

    def __str__(self):
        return f'{self.name}-{self.patient.name}'

    class Meta:
        unique_together = ('name', 'patient')
        verbose_name = 'پزشک'
        verbose_name_plural = 'پزشکان'


class Visit(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='visits')
    doctor = models.ForeignKey(Doctor, null=True, on_delete=models.SET_NULL, related_name='visits')
    doctor_name = models.CharField(max_length=150, null=True)
    reason = models.TextField(max_length=200, verbose_name='دلیل مراجعه')
    visit_date = models.DateField(verbose_name='تاریخ مراجعه')
    next_visit = models.DateField(null=True, blank=True, verbose_name='تاریخ مراجعه بعدی')
    file = models.ImageField(
        upload_to=prescription_img_uploader,
        null=True,
        blank=True,
        verbose_name='تصویر نسخه'
    )
    objects = VisitManager()

    def visit_date_jalali(self):
        return date2jalali(self.visit_date)

    def next_visit_jalali(self):
        return date2jalali(self.next_visit)

    def get_file_url(self):
        try:
            return self.file.url
        except Exception:
            return None

    def __str__(self):
        return f'{self.doctor.name}, {self.patient.name}, {self.visit_date_jalali()}'

    class Meta:
        verbose_name = 'مراجعه'
        verbose_name_plural = 'مراجعات'


class Test(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='tests')
    test_date = models.DateField(verbose_name='تاریخ آزمایش')
    file = models.FileField(upload_to=test_document_uploader,
                            validators=[validate_file_extension],
                            verbose_name='فایل آزمایش')
    objects = TestManager()

    def test_date_jalali(self):
        return date2jalali(self.test_date)

    def __str__(self):
        return str(date2jalali(self.test_date)) + ' ' + 'آزمایش'

    class Meta:
        verbose_name = 'آزمایش'
        verbose_name_plural = 'آزمایش ها'


class OtherDocs(models.Model):
    TYPE_CHOICES = (
        ('sono', 'سونوگرافی'),
        ('img_scan', 'عکس'),
        ('others', 'غیره')
    )
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='docs')
    doc_type = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name='نوع سند')
    title = models.CharField(max_length=100, verbose_name='عنوان')
    file = models.FileField(
        upload_to=other_doc_uploader,
        validators=[validate_file_extension],
        verbose_name='فایل سند'
    )
    doc_date = models.DateField(verbose_name='تاریخ انجام')
    objects = OtherDocsManager()

    def doc_date_jalali(self):
        return date2jalali(self.doc_date)

    def __str__(self):
        return f'{self.doc_type} {self.title}'
