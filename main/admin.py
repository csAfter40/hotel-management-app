from django.contrib import admin
from .models import Currency, Language, Country, User
from manager.models import Owner, Hotel, Floor, Room, Employee, RoomCleaning, RoomRate, RoomType, Bed, RoomBed
from frontdesk.models import HotelLanguages, Guest, Reservation, Folio, Expense

# Register your models here.
admin.site.register(User)
admin.site.register(Currency)
admin.site.register(Language)
admin.site.register(Country)
admin.site.register(Owner)
admin.site.register(Hotel)
admin.site.register(Floor)
admin.site.register(Room)
admin.site.register(Employee)
admin.site.register(RoomCleaning)
admin.site.register(RoomRate)
admin.site.register(HotelLanguages)
admin.site.register(Guest)
admin.site.register(RoomType)
admin.site.register(Bed)
admin.site.register(RoomBed)
admin.site.register(Reservation)
admin.site.register(Folio)
admin.site.register(Expense)
