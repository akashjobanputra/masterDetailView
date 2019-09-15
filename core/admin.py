from django.contrib import admin

from .models import Employee, EmployeeInfo
# Register your models here.

admin.site.register(Employee)
admin.site.register(EmployeeInfo)