from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register([Company, Medicine, MedicalDetail, Employee, Customer, Bill, EmployeeSalary, BillDetail, CustomerRequest, CompanyAccount, CompanyBank, EmployeeBank])

