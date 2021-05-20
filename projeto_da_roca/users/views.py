import datetime

from django.http import HttpResponse

from django.shortcuts import render,redirect,reverse
from django.contrib.auth import login, authenticate 
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm 


# Create your views here.


def list_users(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

def cadastro_cliente(request):
    return render(request, 'cadastro_cliente.html')


def loginPage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,'email ou senha estão incorretos')
        
    return render(request,'registration/login.html')

def home(request):
    return render(request,'home.html')
