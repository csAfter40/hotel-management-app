from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('main.urls')),
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path('frontdesk/', include('frontdesk.urls')),
    path('manager/', include('manager.urls')),
]
