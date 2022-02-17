from django import forms
from .models import Owner, Hotel, Floor, RoomType, Bed, RoomBed

class DateInput(forms.DateInput):
    input_type = 'date'
    

class OwnerRegisterForm(forms.ModelForm):

    class Meta:
        model = Owner
        exclude = ['user']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'date_of_birth': DateInput(attrs = {'class': 'form-control'}),
            'nationality': forms.Select(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }


class HotelCreateForm(forms.ModelForm):

    class Meta:
        model = Hotel
        exclude = ['owner']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.Select(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'address_line_1': forms.TextInput(attrs={'class': 'form-control'}),
            'address_line_2': forms.TextInput(attrs={'class': 'form-control'}),
            'zipcode': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'})
        }
        labels = {
            'name': 'Hotel Name'
        }


class CreateFloorForm(forms.ModelForm):

    class Meta:
        model = Floor
        exclude = ['hotel', 'sort_id']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'})
        }
        labels = {
            'name': 'Floor Name',
            'description': 'Description'
        }

class CreateRoomTypeForm(forms.ModelForm):

    class Meta:
        model = RoomType
        exclude = ['hotel']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'room_size': forms.NumberInput(attrs={'class': 'form-control'}),
            'has_air_con': forms.CheckboxInput(attrs={'class': 'form-check-input', 'type': 'checkbox'}),
            'has_wifi': forms.CheckboxInput(attrs={'class': 'form-check-input', 'type': 'checkbox'}),
            'has_tv': forms.CheckboxInput(attrs={'class': 'form-check-input', 'type': 'checkbox'}),
            'has_fridge': forms.CheckboxInput(attrs={'class': 'form-check-input', 'type': 'checkbox'}),
            'has_hot_water': forms.CheckboxInput(attrs={'class': 'form-check-input', 'type': 'checkbox'}),
        }
        labels = {
            'title': 'Title',
            'description': 'Description',
            'room_size': 'Room Size',
            'has_air_con': 'A/C',
            'has_wifi': 'WiFi',
            'has_tv': 'TV',
            'has_fridge': 'Fridge',
            'has_hot_water': 'Hot Water',
        }

class BedForm(forms.ModelForm):
    class Meta:
        model = Bed
        fields = ['name', 'capacity', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Name',
            'capacity': 'Capacity',
            'description': 'Description'
        }

class RoomBedForm(forms.ModelForm):
    class Meta:
        model = RoomBed
        exclude = ['room_type']
        widgets = {
            'bed': forms.Select(attrs={'class': 'form-control', 'id': 'bed-list'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'})
        }
