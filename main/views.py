from django.shortcuts import render

# Create your views here.
def index(request):
    context = {
        'message': 'Hello world!'
    }
    return render(request, 'main/index.html', context)

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