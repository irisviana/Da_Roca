import datetime

from django.contrib import messages
from django.contrib.auth import login, authenticate,logout
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404,render, redirect,reverse
from django.contrib.auth.hashers import make_password


from .models import ServiceAddress
from .models import User
from .models import DeliveryTime
from .forms import DeliveryTimeForm, ServiceAdressForm, UserForm

# Create your views here.


def list_users(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)


def create_users(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        password = request.POST['password']
        if form.is_valid():
            user = form.save()
            user.password=make_password(password)
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserForm()
    return render(request, '../templates/registration/create_costumer.html', {'form': form})


def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'email ou senha estão incorretos')

    return render(request, 'registration/login.html')


def logout_page(request):
    logout(request)
    return redirect('home')


def home(request):
    return render(request, 'home.html')


class ServiceAddressView:
    @classmethod
    def list_service_address(cls, request, user_id):
        if user_id:
            service_address = ServiceAddress.objects.filter(user=user_id)
        else:
            service_address = ServiceAddress.objects.all()

        return render(request, 'service_address/home.html', {
            "services_address": service_address,
            'user_id': user_id,
        })


    @classmethod
    def create_service_address(cls, request, user_id):
        user = get_object_or_404(User, id=user_id)
        form = ServiceAdressForm()

        if request.method == 'POST':
            form = ServiceAdressForm(request.POST or None)
            if form.is_valid():
                service_address = form.save()
                service_address.user = user
                service_address.save()

                return redirect('list_service_address', user_id=user_id)

            return render(request, '../templates/service_address/create.html',{
                'form': form,
                'user_id': user_id
            })

    @classmethod
    def update_service_address(cls, request, service_address_id):
        service_address = get_object_or_404(ServiceAddress, id=service_address_id)
        user = service_address.user
        form = ServiceAdressForm(instance=service_address)

        if request.method == 'POST':
            form = ServiceAdressForm(request.POST, instance=service_address)
            if form.is_valid:
                service_address = form.save(commit=False)
                service_address.user = user
                service_address.save()

                return redirect(
                    'list_service_address', user_id=service_address.user_id
                )
            
        return render(request, '../templates/service_address/create.html', {
            'form': form,
            'post': service_address,
            'service_address': service_address
        })

    @classmethod
    def delete_service_address(cls, request):
        user_id = None
        if request.method == 'POST':
           service_address_id = request.POST['service_address_id']
           service_address = get_object_or_404(ServiceAddress, id=service_address_id)
           user_id = service_address.user_id

           service_address.delete()
        return redirect('list_service_address', user_id=user_id)


class DeliveryTimeView:
    @classmethod
    def list_delivery_time(cls, request, service_address_id):
        
        if service_address_id:
            delivery_time = DeliveryTime.objects.filter(service_address=service_address_id)
        else:
            delivery_time = DeliveryTime.objects.all()

        return render(request, '../templates/delivery_time/home.html', {
            "delivery_times": delivery_time,
            'service_address_id': service_address_id,
        })

    @classmethod
    def create_delivery_time(cls, request, service_address_id):
        service_address = get_object_or_404(ServiceAddress, id=service_address_id)
        form = DeliveryTimeForm()

        if request.method == 'POST':
            form = DeliveryTimeForm(request.POST or None)
            if form.is_valid():
                delivery_time = form.save()
                delivery_time.service_address = service_address
                delivery_time.save()

                return redirect('list_delivery_time', service_address_id=service_address_id)

        return render(request, '../templates/delivery_time/create.html', {
            'form': form,
            'service_address_id': service_address_id
        })

    @classmethod
    def update_delivery_time(cls, request, delivery_time_id):
        delivery_time = get_object_or_404(DeliveryTime, id=delivery_time_id)
        service_address = delivery_time.service_address
        form = DeliveryTimeForm(instance=delivery_time)

        if request.method == 'POST':
            form = DeliveryTimeForm(request.POST, instance=delivery_time)
            if form.is_valid():
                delivery_time = form.save(commit=False)
                delivery_time.service_address = service_address
                delivery_time.save()

                return redirect(
                    'list_delivery_time', service_address_id=delivery_time.service_address.id)        

        return render(request, '../templates/delivery_time/create.html', {
            'form': form,
            'post': delivery_time,
            'delivery_time': delivery_time
        })

    @classmethod
    def delete_delivery_time(cls, request):
        service_address_id = None
        if request.method == 'POST':
            delivery_time_id = request.POST['delivery_time_id']
            delivery_time = get_object_or_404(DeliveryTime, id=delivery_time_id)
            service_address_id = delivery_time.service_address.id

            delivery_time.delete()

        return redirect('list_delivery_time', service_address_id=service_address_id)
