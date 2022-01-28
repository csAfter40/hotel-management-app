from django.urls import path
from . import views


app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.LoginView.as_view(), name='login'),
    # path('login', views.login_view, name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('register', views.RegisterView.as_view(), name='register'),
    # path('register/guest', views.register_guest, name='register_guest'),
    # path('register/manager', views.register_manager, name='register_manager'),
]
