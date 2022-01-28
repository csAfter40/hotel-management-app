from django.urls import path
from . import views

app_name = 'manager'

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.OwnerRegister.as_view(), name='register'),
    path('add_hotel', views.add_hotel, name='add_hotel'),
    path('hotel/<int:id>', views.detail_hotel, name='detail_hotel'),
    path('hotel/edit/<int:id>', views.edit_hotel, name='edit_hotel'),
    path('add_employee', views.add_employee, name='add_employee'),
    path('employee/<int:id>', views.detail_employee, name='detail_employee'),
    path('employee/edit/<int:id>', views.edit_employee, name='edit_employee'),  
]