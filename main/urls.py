from django.urls import path
from . import views


app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('register', views.RegisterView.as_view(), name='register'),
    path('profile/<pk>/edit', views.EditProfileView.as_view(), name='edit_profile'),
]

htmx_urlpatterns = [
    path('check_username', views.check_username, name='check_username'),
]

urlpatterns += htmx_urlpatterns