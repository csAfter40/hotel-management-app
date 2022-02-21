from functools import wraps
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Hotel
from django.core.exceptions import PermissionDenied
from django.urls import reverse

def hotel_owner_check(function):
    """ Owner checking decorator. Checks if user is owner of the hotel. """
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, 'main/login.html')
        if not hasattr(request.user, 'owner'):
            return HttpResponseRedirect(reverse('main:index'))
        hotel_id = kwargs['hotel_id']
        hotel = Hotel.objects.get(id=hotel_id)
        if not hotel in request.user.owner.hotel_set.all():
            raise PermissionDenied
        return function(request, *args, **kwargs)
    return wrap