from django.db import models

# Create your models here.
""" 
employeeMaster
employeeInformation
 """

GENDER_TYPE = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

class TimeStampModel(models.Model):

    """ 
    Abstract class for all models to store created, updated and
    deleted informarion (Time Manage).
    """

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False, editable=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False, editable=True)
    soft_delete = models.BooleanField(default=False)

    class Meta:
        abstract = True

class Employee(TimeStampModel):

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50, db_index=True)

    def __str__(self):
        return f"{self.name} <{self.email}>"

    class Meta:
        db_table = "employee"

class EmployeeInfo(TimeStampModel):

    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    gender = models.CharField(max_length=2, choices=GENDER_TYPE)
    dob = models.DateField(null=True, blank=True)
    phone = models.BigIntegerField(null=True, blank=True)
    curr_address = models.TextField(null=True, blank=True)
    joining_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.employee.name} <{self.employee.email}>"

    class Meta:
        db_table = "employeeInfo"