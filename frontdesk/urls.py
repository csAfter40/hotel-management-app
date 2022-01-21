from django.urls import path
from . import views

app_name = 'frontdesk'

urlpatterns = [
    path('', views.index, name='index'),
    path('rooms', views.rooms, name='rooms'),
    path('calender', views.calender, name='calender'),
    path('room/<str:room_no>', views.room_detail, name='room_detail'),
]