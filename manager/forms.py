from django import forms
from .models import Owner, Hotel, Floor

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