from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.dispatch import receiver

def upload_to(instance, filename):
    return f'profile_pictures/{instance.user.id}/{filename}'

class User(AbstractUser):
    
    def is_owner(self):
        return hasattr(self, 'owner')

    def __str__(self):
        return self.username


class Currency(models.Model):
    code = models.CharField(max_length=2)
    name = models.CharField(max_length=32)
    symbol = models.CharField(max_length=8, null=True, blank=True)

    def __str__(self):
        return self.code


class Language(models.Model):
    code = models.CharField(max_length=2)
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Country(models.Model):
    code = models.CharField(max_length=2)
    name = models.CharField(max_length=32)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, related_name='countries')
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, related_name='countries')

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    gender_choices = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=32, null=True, blank=True)
    last_name = models.CharField(max_length=32, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=gender_choices, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    nationality = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    profile_picture = models.ImageField('Profile Picture', upload_to=upload_to, default='profile_pictures/default.jpg', null=True, blank=True)

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}({self.user.username})"
        else:
            return self.user.username
# TODO
@ receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    print('kwargs:')
    print(kwargs)
    if created:
        UserProfile.objects.create(user=instance) 