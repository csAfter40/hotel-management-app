from pyexpat import model
from django.db import models
from sqlalchemy import null

from main.models import User
from frontdesk.models import RoomType

# Create your models here.
class Owner(models.Model):
    gender_choices = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    id_type_choices = [
        ('I', 'Id card'),
        ('P', 'passport'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    gender = models.CharField(max_length=1, choices=gender_choices)
    date_of_birth = models.DateField(null=True, blank=True)
    #Can install django countries app https://github.com/SmileyChris/django-countries
    nationality = models.CharField(max_length=64)
    # Can install phone number field app https://github.com/stefanfoulis/django-phonenumber-field
    phone = models.CharField(max_length=15)

class Hotel(models.Model):
    owner = models.ManyToManyField(Owner)
    name = models.CharField(max_length=128)
    #Can install django countries app https://github.com/SmileyChris/django-countries
    country = models.CharField(max_length=32)
    state = models.CharField(max_length=32, null=True, blank=True)
    city = models.CharField(max_length=32)
    address_line_1 = models.CharField(max_length=64)
    address_line_2 = models.CharField(max_length=64, null=True, blank=True)
    zipcode = models.CharField(max_length=16)
    # GPS coordinates?

class Floor(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    floor_name = models.CharField(max_length=32)

class Room(models.Model):

    vacancy_choices = [
        ('V', 'Vacant'),
        ('O', 'Occupied'),
    ]

    cleaning_status_choices = [
        ('C', 'Clean'),
        ('D', 'Dirty'),
    ]

    floor = models.ForeignKey(Floor, null=True, on_delete=models.SET_NULL)
    room_type = models.ForeignKey(RoomType, null=True, on_delete=models.SET_NULL)
    room_name = models.CharField(max_length=16)
    vacansy = models.CharField(max_length=1, choices=vacancy_choices)
    cleaning_status = models.CharField(max_length=1, choices=cleaning_status_choices)
    


class Employee(models.Model):
    employee_type_choices = [
        ('FR', 'Front Desk'),
        ('MD', 'Maid'),
        ('EN', 'Engineer'),
        ('KT', 'Kitchen'),
        ('RS', 'Restaurant'),
        ('MA', 'Maintenance'),
        ('HR', 'Human Resources'),
        ('MN', 'Manager'),
    ]

    gender_choices = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    id_type_choices = [
        ('I', 'Id card'),
        ('P', 'passport'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    gender = models.CharField(max_length=1, choices=gender_choices)
    date_of_birth = models.DateField(null=True, blank=True)
    #Can install django countries app https://github.com/SmileyChris/django-countries
    nationality = models.CharField(max_length=64)
    # Can install phone number field app https://github.com/stefanfoulis/django-phonenumber-field
    phone = models.CharField(max_length=15)


class RoomCleaning(models.Model):
    employee = models.ForeignKey(Employee, null=True, on_delete=models.SET_NULL)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    time = models.DateTimeField(null=True, default=None)

class RoomRate(models.Model):

    currency_choices = [
        ('USD', 'USD'),
        ('EUR', 'EUR'),
    ]

    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    date = models.DateField()
    # Study on currency
    currency = models.CharField(max_length=3, choices=currency_choices)
    amount = models.DecimalField(max_digits=10, decimal_places=2)