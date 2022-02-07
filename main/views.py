from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.db import IntegrityError

# Create your views here.
def index(request):
    context = {
        'message': 'Hello world!'
    }
    return render(request, 'main/index.html', context)

class LoginView(View):
    def get(self, request):
        return render(request, 'main/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # if user is an owner, redirect to manager homepage
                if hasattr(user, 'owner'):
                    return HttpResponseRedirect(reverse('manager:index'))
                return render(request, 'main/index.html')
            return render(request, 'main/login.html', {'message': 'User is not active!'})
        return render(request, 'main/login.html', {'message': 'Invalid username or password.'})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('main:index'))

class RegisterView(View):
    def get(self, request):
        return render(request, 'main/register.html')

    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']

        #Ensure password matches confirmation
        password = request.POST['password']
        confirmation = request.POST['confirmation']
        if password != confirmation:
            return render(request, 'main/register.html', {'message': 'Passwords must match!'})

        #Attempt create new user
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
        except IntegrityError:
            return render(request, 'main/register.html', {'message': 'Username already taken!'})
        login(request, user)
        return HttpResponseRedirect(reverse('main:index'))


def login_view(request):
    context = {

    }
    return render(request, 'main/login.html', context)

def register(request):
    context = {}
    return render(request, 'main/register.html', context)

def register_guest(request):
    pass

def register_manager(request):
    pass