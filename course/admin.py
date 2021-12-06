from django.contrib import admin
from .models import Class, Semester, Warning, Complain
from accounts.models import Grade

# Register your models here.

admin.site.register(Class)
admin.site.register(Semester)
admin.site.register(Grade)
