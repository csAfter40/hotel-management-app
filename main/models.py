from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

class Customer(models.Model):
    first_name = models.CharField(max_length=64)
    middle_name = models.CharField(max_length=64, null=True, blank=True)
    last_name = models.CharField(max_length=64)
    gender = models.CharField(max_length=8, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address_line_1 = models.CharField(max_length=128)
    address_line_2 = models.CharField(max_length=128, null=True, blank=True)
    city = models.CharField(max_length=64)
    zipcode = models.CharField(max_length=32)
    country = models.CharField(max_length=32)
    id_no = models.CharField(max_length=32)
    tel_no = models.CharField(max_length=32)

class Owner(models.Model):
    first_name = models.CharField(max_length=64)
    middle_name = models.CharField(max_length=64, null=True, blank=True)
    last_name = models.CharField(max_length=64)
    gender = models.CharField(max_length=8, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address_line_1 = models.CharField(max_length=128)
    address_line_2 = models.CharField(max_length=128, null=True, blank=True)
    city = models.CharField(max_length=64)
    zipcode = models.CharField(max_length=32)
    country = models.CharField(max_length=32)
    id_no = models.CharField(max_length=32)
    tel_no = models.CharField(max_length=32)



