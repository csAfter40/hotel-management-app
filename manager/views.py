from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import Owner
from .forms import OwnerRegisterForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class OwnerRegister(LoginRequiredMixin, CreateView):
    model = Owner
    form_class = OwnerRegisterForm
    template_name = 'manager/register.html'
    success_url = reverse_lazy('manager:index')
    login_url = reverse_lazy('main:login')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(OwnerRegister, self).form_valid(form)

def index(request):
    return render(request, 'manager/index.html')

def add_hotel(request):
    pass

def detail_hotel(request, id):
    pass

def edit_hotel(request, id):
    pass

def add_employee(request):
    pass

def detail_employee(request, id):
    pass

def edit_employee(request, id):
    pass