from django.urls import path
from . import views

app_name = 'manager'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('register', views.OwnerRegister.as_view(), name='register'),
    path('create_hotel', views.HotelCreate.as_view(), name='create_hotel'),
    path('hotel_manager/<int:id>', views.HotelManagerView.as_view(), name='hotel_manager'),
    path('hotel/<int:id>', views.detail_hotel, name='detail_hotel'),
    path('hotel/edit/<int:id>', views.edit_hotel, name='edit_hotel'),
    path('floor_manager/<int:id>', views.FloorManagerView.as_view(), name='floor_manager'),
    path('floor_manager/edit/<pk>', views.FloorEditView.as_view(), name='floor_edit'),
    path('floor_manager/floor_move', views.floor_move, name='floor_move'),
    path('add_employee', views.add_employee, name='add_employee'),
    path('employee/<int:id>', views.detail_employee, name='detail_employee'),
    path('employee/edit/<int:id>', views.edit_employee, name='edit_employee'),  
]