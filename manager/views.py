from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.views.generic.base import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView, BaseCreateView
from .models import Employee, Floor, Hotel, HotelUser, Owner, RoomType, Bed, RoomBed, Room
from main.models import User
from .forms import OwnerRegisterForm, HotelCreateForm, CreateFloorForm, CreateRoomTypeForm, BedForm, RoomBedForm, CreateRoomForm, CreateEmployeeForm
from .decorators import hotel_owner_check
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import HotelOwnerMixin, IsManagerMixin
from django.db.utils import IntegrityError
from django.contrib.auth.models import Group
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

class HotelEditView(LoginRequiredMixin, IsManagerMixin, UpdateView):
    model = Hotel
    form_class = HotelCreateForm
    template_name = 'manager/edit_hotel.html'
    success_url = reverse_lazy('manager:index')



class IndexView(LoginRequiredMixin, IsManagerMixin, View):

    def get(self, request, *args, **kwargs):
        # hotels = Hotel.objects.filter(owner=self.request.user.owner)
        owner = self.request.user.owner
        hotels = owner.hotel_set.all()
        context = {
            'hotels': hotels
        }
        return render(request, 'manager/index.html', context)


class HotelManagerView(HotelOwnerMixin, View):
    def get(self, request, *args, **kwargs):
        context = {
            'hotel': self.hotel,
        }
        return render(self.request, 'manager/hotel_manager.html', context)


class FloorManagerView(HotelOwnerMixin, CreateView):

    form_class = CreateFloorForm
    
    def get(self, request, *args, **kwargs):
        floors = Floor.objects.get_sorted(hotel=self.hotel)
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

    def form_valid(self, form):
        self.success_url = reverse_lazy('manager:floor_manager', kwargs={'hotel_id':self.hotel.id})
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        floors = Floor.objects.get_sorted(hotel=self.hotel)
        floor = floors.get(id=self.kwargs['pk'])

        context = {
            'floor': floor,
            'create': False,
            'hotel': self.hotel,
            'create_floor_form': self.form_class(instance=floor),
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
        floors = Floor.objects.get_sorted(hotel=hotel)
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


class ObjectMoveView(HotelOwnerMixin, View):
    """Common move view for sortable models"""
    def post(self, request, *args, **kwargs):
        models = {
            'floor': Floor,
            'room': Room
        }
        # floors are sorted in hotel and rooms are sorted in floor.
        parents = {
            'floor': 'hotel',
            'room': 'floor'
        }
        data = json.loads(request.body)
        object_model = data['object']
        object_id = data['object_id']
        direction = data['direction']

        object = models[object_model].objects.get(id=object_id)
        sort_id = object.sort_id
        parent = getattr(object, parents[object_model])
        attrs = {parents[object_model]: parent}
        objects = models[object_model].objects.get_sorted(**attrs)
        if direction == 'up':
            if sort_id > 1:
                # Switch sort_id's of 2 objects. 
                other_object = objects[sort_id-2]
                object.sort_id = 0
                object.save()
                object.sort_id, other_object.sort_id = other_object.sort_id, sort_id
                other_object.save()
                object.save()
                return JsonResponse({}, status=200)
            return JsonResponse({}, status=400)

        elif direction == 'down':
            if sort_id < objects.count():
                # Switch sort_id's of 2 objects. 
                other_object = objects[sort_id]
                object.sort_id = 0
                object.save()
                object.sort_id, other_object.sort_id = other_object.sort_id, sort_id
                other_object.save()
                object.save()
                return JsonResponse({}, status=200)
            return JsonResponse({}, status=400)

        return JsonResponse({}, status=400)


class RoomTypesView(HotelOwnerMixin, View):
    form_class = CreateRoomTypeForm
        
    def get(self, request, *args, **kwargs):
        self.room_type_form = CreateRoomTypeForm()
        self.bed_form = BedForm()
        self.room_bed_form = RoomBedForm()
        beds = Bed.objects.filter(is_general=True).filter(hotel=self.hotel)
        room_types = RoomType.objects.filter(hotel=self.hotel).prefetch_related('room_beds__bed')
        context = {
            'create': True,
            'hotel': self.hotel,
            'room_type_form': self.room_type_form,
            'bed_form': self.bed_form,
            'room_bed_form': self.room_bed_form,
            'room_types': room_types,
            'beds': beds,
        }
        return render(self.request, 'manager/room_types.html', context)
    
    def create_room_beds(self, bed_info, room_type):
        for bed_id, quantity in bed_info.items():
            bed = Bed.objects.get(id=int(bed_id))
            room_bed = RoomBed.objects.create(room_type=room_type, bed=bed, quantity=int(quantity))
            room_bed.save()

    def post(self, request, *args, **kwargs):
        bed_info = json.loads(request.POST['bed_info'])
        form = CreateRoomTypeForm(request.POST)
        if form.is_valid():
            room_type = form.save(commit=False)
            room_type.hotel = self.hotel
            room_type.save()
            self.create_room_beds(bed_info, room_type)
        return HttpResponseRedirect(reverse('manager:room_types', kwargs={'hotel_id': self.hotel.id}))


class RoomTypesEditView(HotelOwnerMixin, UpdateView):

    model = RoomType
    form_class = CreateRoomTypeForm
        
    def setup(self, request, *args, **kwargs):
        """Initialize attributes shared by all view methods."""
        super().setup(request, *args, **kwargs)
        self.room_type = RoomType.objects.get(id=self.kwargs['pk'])
        self.room_beds = self.room_type.room_beds.all()


    def get(self, request, *args, **kwargs):
        beds = Bed.objects.filter(is_general=True).filter(hotel=self.hotel)
        room_types = RoomType.objects.filter(hotel=self.hotel).prefetch_related('room_beds__bed')
        context = {
            'create': False,
            'hotel': self.hotel,
            'room_type_form': CreateRoomTypeForm(instance=self.room_type),
            'room_type': self.room_type,
            'bed_form': BedForm(),
            'room_bed_form': RoomBedForm(),
            'room_types': room_types,
            'beds': beds,
            'room_beds': self.room_beds,
        }
        return render(self.request, 'manager/room_types.html', context)

    def update_room_beds(self):
        # remove deleted room beds
        delete_list = []
        self.bed_info = json.loads(self.request.POST['bed_info'])
        for room_bed in self.room_beds:
            if str(room_bed.bed.id) not in list(self.bed_info.keys()):
                delete_list.append(room_bed.id)
        if delete_list:
            for id in delete_list:
                RoomBed.objects.filter(id=id).delete()

        # modify room beds or create new room beds
        for bed_id, quantity in self.bed_info.items():
            bed = Bed.objects.get(id=int(bed_id))
            room_beds = RoomBed.objects.filter(room_type=self.room_type, bed=bed)
            if len(room_beds) > 0:
                room_bed = room_beds[0]
                room_bed.quantity = int(quantity)
                room_bed.save()
            else:
                room_bed = RoomBed.objects.create(room_type=self.room_type, bed=bed, quantity=int(quantity))
    
    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.success_url = reverse_lazy('manager:room_types', kwargs={'hotel_id':self.hotel.id})
        self.update_room_beds()
        self.object = form.save()
        return super().form_valid(form)
        

class RoomManagerView(HotelOwnerMixin, CreateView):
    model = Room
    form_class = CreateRoomForm
    template_name = 'manager/room_manager.html'
    
    def setup(self, request, *args, **kwargs):
        # if there is pk in the url than it is an update page, otherwise it is a create page.
        pk = kwargs.get('pk', False)
        self.create = not bool(pk)
        self.message = None
        self.batch_message = None
        return super().setup(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        floors = Floor.objects.filter(hotel=self.hotel).prefetch_related('rooms__room_type')
        extra_context = {
            'hotel': self.hotel,
            'floors': floors,
            'create': self.create,
            'batch_form': CreateRoomForm(hotel=self.hotel),
            'message': self.message,
            'batch_message': self.batch_message,
        }
        return super().get_context_data(**extra_context)

    def post(self, request, *args, **kwargs):
        if request.POST['method'] == 'batch':
            return self.batch(request, *args, **kwargs)
        self.object = None
        return super(BaseCreateView, self).post(request, *args, **kwargs)

    def get_form_kwargs(self):
        # hotel object needs to be passed to form
        kwargs = super().get_form_kwargs()
        kwargs.update({'hotel': self.hotel})
        return kwargs

    def form_valid(self, form):
        self.success_url = reverse('manager:room_manager', args=[self.hotel.id])
        if self.create:
            data = form.cleaned_data
            floor = data['floor']
            room_count = Room.objects.filter(floor=floor).count()
            form.instance.sort_id = room_count + 1
        self.object = form.save()
        return super().form_valid(form)
    
    def batch(self, request, *args, **kwargs):
        print(request.POST)
        def validate_room_numbers(data, rooms):
            #check if the numbers are integers
            try:
                from_num = int(data['from'])
                to_num = int(data['to'])
            except:
                self.batch_message = 'Invalid room numbers'
                return self.get(request, *args, **kwargs)
            if to_num < from_num:
                to_num, from_num = from_num, to_num
            #check if any of the room numbers in the given interval collide with the current room numbers in the floor.
            form_room_numbers = [str(i) for i in range(from_num, to_num + 1)]
            for room in rooms:
                if room.name in form_room_numbers:
                    self.batch_message = 'Conflicted room numbers. One or more room numbers already exists.'
            return from_num, to_num

        data = request.POST
        floor = Floor.objects.get(id=data['floor'])
        room_type = RoomType.objects.get(id=data['room_type'])
        rooms = Room.objects.filter(floor=floor)
        from_num, to_num = validate_room_numbers(data, rooms)
        if self.batch_message:
            self.batch_form = self.get_form()
            request.method = 'GET' # prevents single create form from populating with batch create form data
            return self.get(request, *args, **kwargs)
        sort_id = rooms.count() + 1
        for num in range(from_num, to_num+1):
            name = str(num)
            room = Room(name=name, floor=floor, room_type=room_type, sort_id=sort_id)
            room.save()
            sort_id += 1
        return redirect('manager:room_manager', hotel_id=data['id']) 


class RoomEditView(HotelOwnerMixin, UpdateView):
    model = Room
    form_class = CreateRoomForm
    template_name = 'manager/room_manager.html'

    def get_context_data(self, **kwargs):
        floors = Floor.objects.filter(hotel=self.hotel).prefetch_related('rooms__room_type')
        extra_context = {
            'hotel': self.hotel,
            'floors': floors,
        }
        return super().get_context_data(**extra_context)

    def get_success_url(self):
        return reverse('manager:room_manager', args=[self.hotel.id])


class EmployeeManagerView(HotelOwnerMixin, CreateView):
    form_class = CreateEmployeeForm
    template_name = 'manager/employee_manager.html'

    def get_context_data(self, **kwargs):
        employees = Employee.objects.filter(user__hotel=self.hotel)
        extra_context = {
            'employees': employees,
            'create': True,
            'hotel': self.hotel,
        }
        kwargs.update(extra_context)
        return super().get_context_data(**kwargs)

    def get_form_kwargs(self):
        # overriding form kwargs data in order to pass hotel object to the form.
        kwargs = super().get_form_kwargs()
        kwargs.update({'hotel':self.hotel})
        return kwargs

    def form_valid(self, form):
        self.success_url = reverse('manager:employee_manager', kwargs={'hotel_id':self.hotel.id})
        return super().form_valid(form)


class EmployeeEditView(HotelOwnerMixin, UpdateView):
    form_class = CreateEmployeeForm
    model = Employee
    template_name = 'manager/employee_manager.html'
    
    def get_context_data(self, **kwargs):
        employees = Employee.objects.filter(user__hotel=self.hotel)
        extra_context = {
            'create': False,
            'hotel': self.hotel,
            'employees': employees,
        }

        kwargs.update(extra_context)
        return super().get_context_data(**kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'hotel': self.hotel})
        return kwargs

    def form_valid(self, form):
        self.success_url = reverse('manager:employee_manager', kwargs={'hotel_id': self.hotel.id})
        return super().form_valid(form)


class HotelUserView(HotelOwnerMixin, View):

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        hotel_id = kwargs['hotel_id']
        self.hotel = Hotel.objects.get(id=hotel_id)

    def get(self, request, *args, **kwargs):
        context = {
            'hotel': self.hotel
        }
        return render(request, 'manager/create_user.html', context)

    def post(self, request, *arg, **kwargs):
        username = request.POST['username']
        email = request.POST['email']

        #Ensure password matches confirmation
        password = request.POST['password']
        confirmation = request.POST['confirmation']
        if password != confirmation:
            return render(request, 'manager/create_user.html', {
                'message': 'Passwords must match!',
                'hotel': self.hotel
                })

        #Attempt create new user
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            hotel_user = HotelUser.objects.create(user=user, hotel=self.hotel)
            hotel_user.save()
        except IntegrityError:
            return render(request, 'manager/create_user.html', {
                'message': 'Username already taken!',
                'hotel': self.hotel
                })
        return HttpResponseRedirect(reverse('manager:employee_manager', kwargs={'hotel_id': self.hotel.id}))

@hotel_owner_check
def floor_delete(request, *args, **kwargs):

    def edit_sort_ids(hotel, sort_id):
        """
        Sets floor sort ids so that all sort ids can be sorted consecutively like '1, 2, 3 ... n' in a hotel with n floors.
        """
        floors = Floor.objects.get_sorted(hotel=hotel)
        for floor in floors:
            if floor.sort_id>sort_id:
                floor.sort_id -= 1
                floor.save()
    
    if request.method == 'POST':
        floor_id = kwargs['pk']
        floor = Floor.objects.get(id=floor_id)
        hotel = floor.hotel
        sort_id = floor.sort_id
        floor.delete()
        edit_sort_ids(hotel, sort_id)
        floors = hotel.floors.order_by('sort_id')
        context = {
            'floors': floors,
            'hotel': hotel
        }
        return render(request, 'manager/table_floors.html', context)

@hotel_owner_check
def create_bed(request, hotel_id):
    hotel = Hotel.objects.get(id=hotel_id)
    if request.method == 'POST':
        form = BedForm(request.POST)
        if form.is_valid():
            bed = form.save(commit=False)
            bed.hotel = hotel
            bed.save()
            context = {
                'room_bed_form': RoomBedForm()
            }
            return render(request, 'manager/input_beds.html', context, status=200)
        else:
            return JsonResponse({"errors": form.errors}, status=400)

@hotel_owner_check
def room_type_delete(request, *args, **kwargs):
    if request.method == 'POST':
        room_type_id = kwargs['pk']
        hotel_id = kwargs['hotel_id']
        hotel = Hotel.objects.get(id=hotel_id)
        room_type = RoomType.objects.get(id=room_type_id)
        room_type.delete()
        room_types = RoomType.objects.filter(hotel=hotel)
        context = {
           'room_types': room_types,
           'hotel': hotel
        }
        return render(request, 'manager/table_room_types.html', context)

@hotel_owner_check
def room_delete(request, *args, **kwargs):
    def edit_sort_ids(floor, sort_id):
        rooms = Room.objects.get_sorted(floor=floor)
        for room in rooms:
            if room.sort_id > sort_id:
                room.sort_id -= 1
                room.save()

    id = kwargs['pk']
    room = Room.objects.get(id=id)
    if request.method == 'POST':
        floor = room.floor
        hotel = floor.hotel
        sort_id = room.sort_id
        room.delete()
        edit_sort_ids(floor, sort_id)
        rooms = Room.objects.get_sorted(floor=floor)
        context = {
            'hotel': hotel,
            'rooms': rooms,
            'floor': floor
        }
        return render(request, 'manager/table_rooms.html', context)
    else:
        return JsonResponse({"errors": f"Can't delete room {room.name}"}, status=400)

@hotel_owner_check
def employee_delete(request, *args, **kwargs):
    if request.method == 'POST':
        employee_id = kwargs['pk']
        hotel_id = kwargs['hotel_id']
        employee = Employee.objects.get(id=employee_id)
        employee.delete()
        context = {
            'employees': Employee.objects.all(),
            'hotel': Hotel.objects.get(id=hotel_id)
        }
        return render(request, 'manager/table_employees.html', context)

@hotel_owner_check
def check_hotel_user(request, *args, **kwargs):
    # if request.POST:
    #     print(request)
    # hotel_id = kwargs['hotel_id']
    data = json.loads(request.body)
    user_id = data['user']
    hotel_user = HotelUser.objects.get(id=user_id)
    # hotel = Hotel.objects.get(id=id)
    print(hotel_user)
    employees = Employee.objects.filter(user=hotel_user)
    if employees.count() == 0:
        return HttpResponse(status=200)
    return HttpResponse(status=409)

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