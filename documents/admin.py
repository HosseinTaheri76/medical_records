from django.contrib import admin
from.models import Doctor, Visit, Test, OtherDocs
# Register your models here.
admin.site.register(Doctor)
admin.site.register(Visit)
admin.site.register(Test)
admin.site.register(OtherDocs)