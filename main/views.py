from django.shortcuts import render

# Create your views here.
def index(request):
    context = {
        'message': 'Hello world!'
    }
    return render(request, 'main/index.html', context)

def login_view(request):
    pass

def register_guest(request):
    pass

def register_manager(request):
    pass