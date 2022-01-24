from django.db import models
from django_countries.fields import CountryField


class HotelLanguages(models.Model):
    language_choices = [
        ('EN', 'English'),
        ('RU', 'Russian'),
        ('DE', 'German'),
    ]
    hotel = models.ForeignKey('manager.Hotel', on_delete=models.CASCADE)
    language = models.CharField(max_length=2, choices=language_choices)


class Guest(models.Model):

    gender_choices = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    # Study on choices
    guest_type_choices = [
        ('FT', 'First Timer'),
        ('VIP', 'VIP')
    ]

    id_type_choices = [
        ('I', 'Id card'),
        ('P', 'passport'),
    ]

    user = models.ForeignKey('main.User', null=True, on_delete=models.SET_NULL)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    gender = models.CharField(max_length=1, choices=gender_choices)
    language = models.ForeignKey(HotelLanguages, on_delete=models.SET_NULL, null=True, blank=True) # Study on language
    guest_type = models.CharField(max_length=16, choices=guest_type_choices)
    date_of_birth = models.DateField(null=True, blank=True)
    id_type = models.CharField(max_length=16, choices=id_type_choices)
    id_number = models.CharField(max_length=32)
    #Can install django countries app https://github.com/SmileyChris/django-countries
    nationality = CountryField()
    # Can install phone number field app https://github.com/stefanfoulis/django-phonenumber-field
    phone = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class RoomType(models.Model):
    title = models.CharField(max_length=32, unique=True)
    hotel = models.ForeignKey('manager.Hotel', on_delete=models.CASCADE, related_name='room_types')

    def __str__(self):
        return self.title



class Reservation(models.Model):
    status_choices = [
        ('RES', 'reserved'),
        ('CAN', 'cancelled'),
        ('ARR', 'arrival'),
        ('CIN', 'checked in'),
        ('DEP', 'departure'),
        ('OUT', 'checked out'),
        ('NOS', 'no show'),
    ]

    meal_choices = [
        ('EP', 'Europen Plan'),
        ('AP', 'American Plan'),
        ('MAP', 'Modified American Plan'),
        ('CP', 'Continental Plan'),
    ]

    source_choices = [
        ('WEB', "website"),
        ('TEL', 'telephone'),
        ('BOO', 'booking.com'),
        ('HOT', 'hotels.com'),
    ]

    rate_plan_choices = [
        ('NOR', 'normal'),
        ('PRO', 'promotion')
    ]

    status = models.CharField(max_length=3, choices=status_choices, default=status_choices[0])
    arrival_date = models.DateField()
    departure_date = models.DateField()
    time_created = models.DateTimeField(auto_now_add=True)
    guest = models.ForeignKey(Guest, null=True, on_delete=models.SET_NULL)
    hotel = models.ForeignKey('manager.Hotel', on_delete=models.CASCADE)
    room_type = models.ForeignKey(RoomType, null=True, on_delete=models.SET_NULL)
    meal_plan = models.TextField(max_length=3, choices=meal_choices)
    adult_qty = models.PositiveSmallIntegerField()
    child_qty = models.PositiveSmallIntegerField(default=0)
    source = models.CharField(max_length=3, choices=source_choices)
    # Study on rate plan
    rate_plan = models.CharField(max_length=3, choices=rate_plan_choices)

    def __str__(self):
        return f"{self.guest} from {self.arrival_dater} to {self.departure_date}"

class Folio(models.Model):
    reservation = models.OneToOneField(Reservation, related_name='folio', on_delete=models.CASCADE)

class Expense(models.Model):

    currency_choices = [
        ('USD', 'USD'),
        ('EUR', 'EUR'),
    ]

    title = models.CharField(max_length=128)
    currency = models.CharField(max_length=3, choices=currency_choices)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    folio = models.ForeignKey(Folio, related_name='expenses', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} {self.amount}{self.currency}"