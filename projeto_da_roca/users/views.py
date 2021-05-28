import datetime

from django.contrib import messages
from django.contrib.auth import login, authenticate,logout
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404,render, redirect,reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from .models import ServiceAddress
from .models import User
from .models import DeliveryTime
from .forms import DeliveryTimeForm, UserForm

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

def admin_home(request):
    return render(request, 'admin/home.html')

def list_admin(request):
        admins = User.objects.all()

        return render(request, 'admin/manage_admin.html', {
            "admins": admins,
        })
def add_admin( request):
    message = ''
    
    users = User.objects.all()

    return render(request, 'admin/add_admin.html', {
            "users": users ,
    })

def seller_home(request):
    return render(request, 'seller/home_seller.html')
    
def request_seller(request):
    if request.method == 'POST':
        sale_description = request.POST['sale_description']
        if(sale_description is None):
            messages.error(request, 'A descrição é o obrigatoria!')
        else:
            if request.user.is_authenticated:
                user = request.user
                user.is_seller = 2 #request permision
                user.sale_description = sale_description
                user.save()
                
    return render(request, 'seller/home_seller.html')

def manage_seller(request):
    sellers = User.objects.filter(is_seller=2)
    return render(request, 'seller/manage_request_seller.html', {
            "sellers": sellers ,
    })
def view_seller_request(request,user_id):

    user = User.objects.get(pk= user_id)
    return render(request, 'seller/view_request_seller.html', {
            "user": user ,
    })

def refuse_seller_request(request):
    service_address_id = None
    if request.method == 'POST':
        user_id = request.POST['user_id']
        user = User.objects.get(pk= user_id)
        user.is_seller=1
        user.save()

    return HttpResponseRedirect(reverse('seller_manage'))

def approve_seller_request(request):
    service_address_id = None
    if request.method == 'POST':
        user_id = request.POST['user_id']
        user = User.objects.get(pk= user_id)
        user.is_seller=0
        user.save()

    return HttpResponseRedirect(reverse('seller_manage'))

class ServiceAddressView:
    @classmethod
    def list_service_address(cls, request):
        service_address = ServiceAddress.objects.all()

        return render(request, 'service_address/home.html', {
            "services_address": service_address,
        })


    @classmethod
    def create_service_address(cls, request):
        message = ''
        if request.method == 'POST':
            city = request.POST['cidade']
            state = request.POST['estado']
            #userId = request.POST['usuarioId']

            #user = User.objects.get(id = userId)
            if request.user.is_authenticated:
                user= request.user
                service_address = ServiceAddress(
                    user=user, city=city, state=state)

                service_address.save()

                message = "Endereço de atendimento criado com sucesso."
                service_address = ServiceAddress.objects.all()
            return HttpResponseRedirect(reverse('list_service_address'))
            
        
        return render(request, 'service_address/create.html', {
            'message': message,
        })

    @classmethod
    def update_service_address(cls, request):
        message = ''
        if request.method == 'POST':
            service_address_id = request.POST['enderecoEntredaId']
            city = request.get('cidade')
            state = request.get('estado')
            
            service_address = ServiceAddress.objects.get(id=service_address_id)
            
            service_address.update(
                city=city if city else service_address.city,
                state=state if state else service_address.state)

            message = "Endereço de atendimento atualizado com sucesso."

        return render(request, 'usuario/service_address/create.html', {
            'mesage': message,
        })

    @classmethod
    def delete_service_address(cls, request):
        message = ''
        if request.method == 'POST':
            service_address_id = request.POST['service_address_id']
            
            try:
                service_address = ServiceAddress.objects.get(id=service_address_id)
                service_address.delete()

                message = "Endereço de atendimento deletado com sucesso."
            except ServiceAddress.DoesNotExist as e:
                print(str(e)) 
                message = 'Endereço de entrega não existe.'

            services_address = ServiceAddress.objects.all()
            
        return HttpResponseRedirect(reverse('list_service_address'))

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
