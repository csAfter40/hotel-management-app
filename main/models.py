from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    
    def __str__(self):
        return self.username

class Currency(models.Model):
    code = models.CharField(max_length=2)
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

class Language(models.Model):
    code = models.CharField(max_length=2)
    name = models.CharField(max_length=32)
    symbol = models.CharField(max_length=8, null=True, blank=True)

    def __str__(self):
        return self.code

class Country(models.Model):
    code = models.CharField(max_length=2)
    name = models.CharField(max_length=32)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, related_name='countries')
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, related_name='countries')

    def __str__(self):
        return self.name

