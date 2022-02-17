from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Owner(models.Model):
    gender_choices = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    id_type_choices = [
        ('I', 'Id card'),
        ('P', 'passport'),
    ]

    user = models.OneToOneField('main.User', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    gender = models.CharField(max_length=1, choices=gender_choices)
    date_of_birth = models.DateField(null=True, blank=True)
    nationality = models.ForeignKey('main.Country', on_delete=models.SET_NULL, null=True, related_name='owners')
    # Phone number field app https://github.com/stefanfoulis/django-phonenumber-field
    phone_number = PhoneNumberField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Hotel(models.Model):
    owners = models.ManyToManyField(Owner)
    name = models.CharField(max_length=128)
    country = models.ForeignKey('main.Country', on_delete=models.SET_NULL, null=True, related_name='hotels')
    state = models.CharField(max_length=32, null=True, blank=True)
    city = models.CharField(max_length=32)
    address_line_1 = models.CharField(max_length=64)
    address_line_2 = models.CharField(max_length=64, null=True, blank=True)
    zipcode = models.CharField(max_length=16)
    email = models.EmailField(max_length=256)
    phone_number = PhoneNumberField()
    # GPS coordinates?

    def __str__(self):
        return self.name


class Floor(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='floors')
    sort_id = models.IntegerField(blank=True, default=1)
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=128, null=True, blank=True)

    class Meta:
        unique_together = [['hotel', 'sort_id']]

    def __str__(self):
        return self.name


class Bed(models.Model):
    name = models.CharField(max_length=64)
    capacity = models.PositiveSmallIntegerField()
    description = models.CharField(max_length=64, null=True, blank=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='beds', null=True, blank=True) # for custom defined beds.
    is_general = models.BooleanField(default=False) # for general use beds.

    def __str__(self):
        return self.name


class RoomType(models.Model):
    title = models.CharField(max_length=32, unique=True)
    description = models.CharField(max_length=512, null=True, blank=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='room_types')
    room_size = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    # Room features
    has_air_con = models.BooleanField(default=False, verbose_name="A/C")
    has_wifi = models.BooleanField(default=False, verbose_name="wifi")
    has_tv = models.BooleanField(default=False, verbose_name="TV")
    has_fridge = models.BooleanField(default=False, verbose_name="fridge")
    has_hot_water = models.BooleanField(default=False, verbose_name="hot water")


    def __str__(self):
        return self.title


class RoomBed(models.Model):
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    bed = models.ForeignKey(Bed, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.quantity} x {self.name}'


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
    
    def __str__(self):
        return self.room_name


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

    user = models.ForeignKey('main.User', on_delete=models.CASCADE)
    employee_type = models.CharField(max_length=2, choices=employee_type_choices)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    gender = models.CharField(max_length=1, choices=gender_choices)
    date_of_birth = models.DateField(null=True, blank=True)
    nationality = models.ForeignKey('main.Country', on_delete=models.SET_NULL, null=True)
    # Phone number field app https://github.com/stefanfoulis/django-phonenumber-field
    phone_number = PhoneNumberField()

    def __str__(self):
        return self.employee_type, self.first_name, self.last_name


class RoomCleaning(models.Model):
    employee = models.ForeignKey(Employee, null=True, on_delete=models.SET_NULL)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    time = models.DateTimeField(null=True, default=None)

    def __str__(self):
        return f"{self.room} -> {self.employee}"


class RoomRate(models.Model):
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    date = models.DateField()
    currency = models.ForeignKey('main.Currency', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=14, decimal_places=2)

    def __str__(self):
        return self.rate