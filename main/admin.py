from django.contrib import admin
from .models import Currency, Language, Country
from manager.models import Owner, Hotel, Floor, Room, Employee, RoomCleaning, RoomRate
from frontdesk.models import HotelLanguages, Guest, RoomType, Reservation, Folio, Expense

# Register your models here.
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
admin.site.register(Reservation)
admin.site.register(Folio)
admin.site.register(Expense)
