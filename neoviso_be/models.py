from django.contrib.auth.models import User
from django.db import models


class Customer(models.Model):
    fullname = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    department = models.ForeignKey('Department', on_delete=models.CASCADE)


class Department(models.Model):
    fullname = models.CharField(max_length=255)
    address = models.CharField(max_length=200)


class Appointment(models.Model):
    date = models.DateField()
    start = models.TimeField()
    end = models.TimeField()
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)

    class Meta:
        permissions = [
            ('change_own_appointment', 'Can change own appointment'),
            ('change_other_appointment', 'Can change other appointment'),
            ('delete_own_appointment', 'Can delete own appointment'),
            ('delete_other_appointment', 'Can delete other appointment')
        ]
