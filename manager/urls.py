from django.urls import path
from . import views

app_name = 'manager'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('register', views.OwnerRegister.as_view(), name='register'),
    path('create_hotel', views.HotelCreate.as_view(), name='create_hotel'),
    path('<int:hotel_id>/hotel_manager', views.HotelManagerView.as_view(), name='hotel_manager'),
    path('hotel/<int:id>', views.detail_hotel, name='detail_hotel'),
    path('hotel/edit/<int:id>', views.edit_hotel, name='edit_hotel'),
    path('<int:hotel_id>/floor_manager', views.FloorManagerView.as_view(), name='floor_manager'),
    path('<int:hotel_id>/floor_manager/edit/<pk>', views.FloorEditView.as_view(), name='floor_edit'),
    path('<int:hotel_id>/floor_manager/floor_move', views.ObjectMoveView.as_view(), name='floor_move'),
    path('<int:hotel_id>/room_manager', views.RoomManagerView.as_view(), name='room_manager'),
    path('<int:hotel_id>/room_manager/edit/<pk>', views.RoomEditView.as_view(), name='room_edit'),
    path('<int:hotel_id>/room_manager/room_move', views.ObjectMoveView.as_view(), name='room_move'),
    path('<int:hotel_id>/room_types', views.RoomTypesView.as_view(), name='room_types'),
    path('<int:hotel_id>/room_types/edit/<pk>', views.RoomTypesEditView.as_view(), name='room_types_edit'),
    path('<int:hotel_id>/employee_manager', views.EmployeeManagerView.as_view(), name='employee_manager'),
    path('<int:hotel_id>/employee_manager/edit/<pk>', views.EmployeeEditView.as_view(), name='employee_edit'),
    path('<int:hotel_id>/employee_manager/hotel_user', views.HotelUserView.as_view(), name='hotel_user'),
    path('add_employee', views.add_employee, name='add_employee'),
    path('employee/<int:id>', views.detail_employee, name='detail_employee'),
    path('employee/edit/<int:id>', views.edit_employee, name='edit_employee'),  
]

htmx_urlpatterns = [
    path('<int:hotel_id>/floor_manager/del/<int:pk>', views.floor_delete, name='floor_delete'),
    path('<int:hotel_id>/room_types/del/<int:pk>', views.room_type_delete, name='room_type_delete'),
    path('<int:hotel_id>/room_manager/del/<int:pk>', views.room_delete, name='room_delete'),
    path('<int:hotel_id>/employee_manager/del/<int:pk>', views.employee_delete, name='employee_delete'),
    path('<int:hotel_id>/create_bed', views.create_bed, name='create_bed'),
]

urlpatterns += htmx_urlpatterns