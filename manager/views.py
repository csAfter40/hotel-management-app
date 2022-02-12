from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.generic.base import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Floor, Hotel, Owner
from .forms import OwnerRegisterForm, HotelCreateForm, CreateFloorForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import HotelOwnerMixin, IsManagerMixin, OwnerCheckMixin
from django.db.utils import IntegrityError
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
import json

class OwnerRegister(LoginRequiredMixin, CreateView):
    model = Owner
    form_class = OwnerRegisterForm
    template_name = 'manager/register.html'
    success_url = reverse_lazy('manager:index')

    # Sets user field for owner and adds owners group to user
    def form_valid(self, form):
        form.instance.user = self.request.user
        group = Group.objects.get(name='owners')
        self.request.user.groups.add(group)
        return super(OwnerRegister, self).form_valid(form)

    # Handling integrity errors in case user tries to create a second owner
    def post(self, request, *args, **kwargs):
        try:
            return super(OwnerRegister, self).post(request, *args, **kwargs)
        except IntegrityError:
            context = super().get_context_data(**kwargs)
            context['message'] = 'You already registered an owner with this user.'
            return render(request, template_name=self.template_name, context=context)


class HotelCreate(LoginRequiredMixin, IsManagerMixin, CreateView):
    model = Hotel
    form_class = HotelCreateForm
    template_name = 'manager/create_hotel.html'
    success_url = reverse_lazy('manager:index')

    # Set user as hotel owner
    def form_valid(self, form):
        hotel = form.save() # Form has to be saved before adding object to a many to many field.
        owner = self.request.user.owner
        hotel.owners.add(owner)
        return super(HotelCreate, self).form_valid(form)


class IndexView(LoginRequiredMixin, IsManagerMixin, View):

    def get(self, request, *args, **kwargs):
        # hotels = Hotel.objects.filter(owner=self.request.user.owner)
        owner = self.request.user.owner
        hotels = owner.hotel_set.all()
        print(hotels)
        context = {
            'hotels': hotels
        }
        return render(request, 'manager/index.html', context)


class HotelManagerView(HotelOwnerMixin, View):
    def get(self, request, *args, **kwargs):
        id = self.kwargs['hotel_id']
        hotel = Hotel.objects.get(id=id)
        context = {
            'hotel': hotel,
        }
        return render(self.request, 'manager/hotel_manager.html', context)


class FloorManagerView(HotelOwnerMixin, CreateView):

    form_class = CreateFloorForm
    
    def setup(self, request, *args, **kwargs):
        """Initialize attributes shared by all view methods."""
        if hasattr(self, 'get') and not hasattr(self, 'head'):
            self.head = self.get
        self.request = request
        self.args = args
        self.kwargs = kwargs
        id = kwargs['hotel_id']
        self.hotel = Hotel.objects.get(id=id)

    def get(self, request, *args, **kwargs):
        floors = Floor.objects.filter(hotel=self.hotel).order_by('sort_id')
        context = {
            'create': True,
            'hotel': self.hotel,
            'create_floor_form': self.form_class,
            'floors': floors
        }
        return render(self.request, 'manager/floor_manager.html', context)

    def form_valid(self, form):
        form.instance.hotel = self.hotel
        floor_count = self.hotel.floors.count()
        form.instance.sort_id = floor_count + 1
        form.save()
        return HttpResponseRedirect(reverse_lazy('manager:floor_manager', kwargs={'hotel_id':self.hotel.id}))


class FloorEditView(HotelOwnerMixin, UpdateView):

    model = Floor
    form_class = CreateFloorForm
    
    
    def setup(self, request, *args, **kwargs):
        """Initialize attributes shared by all view methods."""
        if hasattr(self, 'get') and not hasattr(self, 'head'):
            self.head = self.get
        self.request = request
        self.args = args
        self.kwargs = kwargs
        pk = kwargs['pk']
        self.floor = Floor.objects.get(id=pk)
        self.hotel = self.floor.hotel
        self.success_url = reverse_lazy('manager:floor_manager', kwargs={'hotel_id':self.hotel.id})

    def get(self, request, *args, **kwargs):
        floors = Floor.objects.filter(hotel=self.hotel).order_by('sort_id')

        context = {
            'floor': self.floor,
            'create': False,
            'hotel': self.hotel,
            'create_floor_form': self.form_class(instance=self.floor),
            'floors': floors
        }
        return render(self.request, 'manager/floor_manager.html', context)


class FloorDeleteView(HotelOwnerMixin, DeleteView):
    
    model = Floor
    
    def get_queryset(self):
        """
        Returns only the floors which user is in the owners of the hotel in which the floor is created.
        """
        queryset = super(FloorDeleteView, self).get_queryset()
        return queryset.filter(hotel__in=self.request.user.owner.hotel_set.all())

    def edit_sort_ids(self, hotel, sort_id):
        """
        Sets floor sort ids so that all sort ids can be sorted consecutively like '1, 2, 3 ... n' in a hotel with n floors.
        """
        floors = Floor.objects.filter(hotel=hotel)
        for floor in floors:
            if floor.sort_id>sort_id:
                floor.sort_id -= 1
                floor.save()

    # Django 4.0 requires form_valid method to be overriden not delete method.
    def form_valid(self, form):
        """
        Overriden the form_valid method so that edit_sort_ids method will be called after deleting the object.
        """
        self.object = self.get_object()
        hotel = self.object.hotel
        sort_id = self.object.sort_id
        self.object.delete()
        self.edit_sort_ids(hotel, sort_id)
        return JsonResponse({}, status=200)


class FloorMoveView(HotelOwnerMixin, View):

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        floor_id = data['floor_id']
        direction = data['direction']

        floor = Floor.objects.get(id=floor_id)
        sort_id = floor.sort_id
        hotel = floor.hotel
        # Check if the user is in owners of the hotel
        if not request.user.is_owner() or request.user.owner not in hotel.owners.all():
            return JsonResponse({}, status=400)
        floors = Floor.objects.filter(hotel=hotel).order_by('sort_id')

        if direction == 'up':
            if sort_id > 1:
                # Switch sort_id's of 2 floors. 
                other_floor = floors[sort_id-2]
                floor.sort_id = 0
                floor.save()
                floor.sort_id, other_floor.sort_id = other_floor.sort_id, sort_id
                other_floor.save()
                floor.save()
                return JsonResponse({}, status=200)
            return JsonResponse({}, status=400)

        elif direction == 'down':
            print(sort_id)
            if sort_id < floors.count():
                # Switch sort_id's of 2 floors. 
                other_floor = floors[sort_id]
                floor.sort_id = 0
                floor.save()
                floor.sort_id, other_floor.sort_id = other_floor.sort_id, sort_id
                other_floor.save()
                floor.save()
                return JsonResponse({}, status=200)
            return JsonResponse({}, status=400)

        return JsonResponse({}, status=400)


class RoomTypesView(HotelOwnerMixin, View):

    def get(self, request, *args, **kwargs):
        id = kwargs['hotel_id']
        hotel = Hotel.objects.get(id=id)
        context = {
            'hotel': hotel
        }
        return render(request, 'manager/room_types.html', context)


class RoomManagerView(HotelOwnerMixin, View):

    def get(self, request, *args, **kwargs):
        id = kwargs['hotel_id']
        hotel = Hotel.objects.get(id=id)
        context = {
            'hotel': hotel
        }
        return render(request, 'manager/room_manager.html', context)


def detail_hotel(request, id):
    pass

def edit_hotel(request, id):
    pass

def add_manager_to_hotel(request):
    pass

def add_employee(request):
    pass

def detail_employee(request, id):
    pass

def edit_employee(request, id):
    pass