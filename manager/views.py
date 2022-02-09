from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import View
from django.views.generic.edit import CreateView, FormMixin
from .models import Floor, Hotel, Owner
from .forms import OwnerRegisterForm, HotelCreateForm, CreateFloorForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import IsManagerMixin
from django.db.utils import IntegrityError
from django.contrib.auth.models import Group


class OwnerRegister(LoginRequiredMixin, CreateView):
    model = Owner
    form_class = OwnerRegisterForm
    template_name = 'manager/register.html'
    success_url = reverse_lazy('manager:index')
    # login_url = reverse_lazy('main:login')

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
    # login_url = reverse_lazy('main:login')

    # Set user as hotel owner
    def form_valid(self, form):
        hotel = form.save() # Form has to be saved before adding object to a many to many field.
        owner = self.request.user.owner
        hotel.owner.add(owner)
        return super(HotelCreate, self).form_valid(form)


class IndexView(LoginRequiredMixin, IsManagerMixin, View):
    # login_url = reverse_lazy('main:login')

    def get(self, request, *args, **kwargs):
        hotels = Hotel.objects.filter(owner=self.request.user.owner)
        print(hotels)
        context = {
            'hotels': hotels
        }
        return render(request, 'manager/index.html', context)


class FloorManagerView(LoginRequiredMixin, IsManagerMixin, CreateView):

    model = Floor
    form_class = CreateFloorForm
    template_name = 'manager/floor_manager.html'
    # success_url = reverse_lazy('manager:floor_manager', kwargs={'id':2})
    
    def get(self, request, *args, **kwargs):
        id = kwargs['id']
        hotel = Hotel.objects.get(id=id)
        floors = Floor.objects.all().order_by('sort_id')
        context = {
            'hotel': hotel,
            'create_floor_form': CreateFloorForm(),
            'floors': floors
        }
        return render(self.request, 'manager/floor_manager.html', context)

    def form_valid(self, form):
        id = self.request.POST['id']
        hotel = Hotel.objects.get(id=id)
        form.instance.hotel = hotel
        form.save()
        return HttpResponseRedirect(reverse_lazy('manager:floor_manager', kwargs={'id':id}))




class HotelManagerView(LoginRequiredMixin, IsManagerMixin, View):

    def get(self, request, *args, **kwargs):
        id = self.kwargs['id']
        hotel = Hotel.objects.get(id=id)
        context = {
            'hotel': hotel,
        }
        return render(self.request, 'manager/hotel_manager.html', context)

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