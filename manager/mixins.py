import http
from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Hotel

class IsManagerMixin(AccessMixin):
    """If user is not manager, decline permission"""

    def dispatch(self, request, *args, **kwargs):
        """If user is not authenticated and manager permission will be denied"""
        user = request.user
        if user.is_authenticated and hasattr(user, 'owner'):
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('main:index')) 


class OwnerCheckMixin:

    def dispatch(self, request, *args, **kwargs):
        id = kwargs['hotel_id']
        hotel = Hotel.objects.get(id=id)
        if hotel in request.user.owner.hotel_set.all():
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

class HotelOwnerMixin(AccessMixin):
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not hasattr(request.user, 'owner'):
            return HttpResponseRedirect(reverse('main:index'))
        id = kwargs['hotel_id']
        hotel = Hotel.objects.prefetch_related('owners').get(id=id)
        if not hasattr(self, 'hotel'):
            self.hotel = hotel
        if not request.user.owner in hotel.owners.all():
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)