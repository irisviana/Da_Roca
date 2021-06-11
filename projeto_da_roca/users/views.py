from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect, reverse

from .forms import DeliveryTimeForm, ServiceAddressForm, UserForm, AddressForm, UserUpdateForm
from .models import DeliveryTime
from .models import ServiceAddress
from .models import User
from .models import Address

# Create your views here.


class UserView:
    @classmethod
    def list_users(cls, request, user_type='all'):
        if request.user.is_authenticated:
            users = User.objects.filter(is_active=True)
            if request.method == 'GET':
                if user_type == 'admin':
                    users = users.filter(is_admin=True)
                elif user_type == 'client':
                    users = users.filter(is_admin=False, is_seller=False)
                elif user_type == 'producer':
                    users = users.filter(is_seller=True)

            return render(request, 'user/manage_users.html', {
                "users": users,
                "user_type": user_type
            })
        return redirect('login')

    @classmethod
    def create_users(cls, request):
        if request.method == 'POST':
            form = UserForm(request.POST)
            password = request.POST['password']
            if form.is_valid():
                user = form.save()
                user.password = make_password(password)
                user.save()
                login(request, user)
                return redirect('home')
        else:
            form = UserForm()
        return render(request, 'registration/create_customer.html', {'form': form})

    @classmethod
    def update_users(cls, request):
        if request.user.is_authenticated:
            user = request.user
            form = UserUpdateForm(instance=user)

            if request.method == 'POST':
                form = UserUpdateForm(request.POST, instance=user)
                if form.is_valid():
                    user = form.save()

                    message = 'Atualizado com sucesso.'
                    return render(request, '../templates/registration/update_customer.html', {
                        'form': form,
                        'message': message
                    })

        return render(request, '../templates/registration/update_customer.html', {'form': form})

    @classmethod
    def self_delete(cls, request):
        if request.user.is_authenticated:
            auth_user = request.user
            if request.method == 'POST':
                user = User.objects.get(username=auth_user.username)
                user.is_active = False
                user.save()
                return redirect('logout')
            return redirect('home')

        return redirect('login')

    @classmethod
    def delete_user(cls, request):
        if request.user.is_authenticated:
            user_type = 'all'
            if request.method == 'POST':
                user_type = request.POST.get('user_type', 'all')
                user_id = request.POST.get('user_id')
                user = User.objects.get(pk=user_id)
                user.is_active = False
                user.save()

            return redirect('manage_user', user_type=user_type)
        return redirect('login')

    @classmethod
    def remove_admin(cls, request):
        if request.user.is_authenticated:
            user_type = 'all'
            if request.method == 'GET':
                user_type = request.GET.get('user_type', 'all')
                admin_id = request.GET.get('admin_id')
                user = User.objects.get(pk=admin_id)
                user.is_admin = False
                user.save()

            return redirect('manage_user', user_type=user_type)
        return redirect('login')

    @classmethod
    def refuse_seller_request(cls, request):
        if request.user.is_authenticated:
            user_type = 'all'
            if request.method == 'GET':
                user_type = request.GET.get('user_type', 'all')
                user_id = request.GET.get('user_id')
                user = User.objects.get(pk=user_id)
                user.is_seller = False
                user.seller_status = 'R'
                user.save()

            return redirect('manage_user', user_type=user_type)
        return redirect('login')

    @classmethod
    def login_page(cls, request):
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('customer_home')
            else:
                messages.error(request, 'email ou senha estão incorretos')

        return render(request, 'registration/login.html')

    @classmethod
    def logout_page(cls, request):
        if request.user.is_authenticated:
            logout(request)
            return redirect('home')
        return redirect('login')

    def customer_home_first(request):
        if request.user.is_authenticated:
            return redirect('update_customer', request.user.username)
        return redirect('login')

    def customer_home(request):
        if request.user.is_authenticated:
            return render(request, 'users_profile/customer_home_base.html')
        return redirect('login')

    @classmethod
    def home(cls, request):
        return render(request, 'home.html')

    @classmethod
    def admin_home(cls, request):
        if request.user.is_authenticated:
            return render(request, 'user/home.html')
        return redirect('login')

    @classmethod
    def add_admin(cls, request):
        if request.user.is_authenticated:
            users = User.objects.filter(is_admin=False)

            return render(request, 'user/add_admin.html', {
                "users": users,
            })
        return redirect('login')

    @classmethod
    def seller_home(cls, request):
        if request.user.is_authenticated:
            return render(request, 'seller/home_seller.html')
        return redirect('login')

    @classmethod
    def request_seller(cls, request):
        if request.user.is_authenticated:
            if request.method == 'POST':
                sale_description = request.POST['sale_description']
                if (sale_description is None):
                    messages.error(request, 'A descrição é o obrigatoria!')
                else:
                    if request.user.is_authenticated:
                        user = request.user
                        user.seller_status = 'P'  # request permision
                        user.sale_description = sale_description
                        user.save()

            return render(request, 'seller/home_seller.html')
        return redirect('login')

    @classmethod
    def manage_seller(cls, request):
        if request.user.is_authenticated:
            sellers = User.objects.filter(seller_status='P')
            return render(request, 'seller/manage_request_seller.html', {
                "sellers": sellers,
            })
        return redirect('login')

    @classmethod
    def view_seller_request(cls, request, user_id):
        if request.user.is_authenticated:
            user = User.objects.get(pk=user_id)
            return render(request, 'seller/view_request_seller.html', {
                "user": user,
            })
        return redirect('login')

    @classmethod
    def approve_seller_request(cls, request):
        if request.user.is_authenticated:
            if request.method == 'POST':
                user_id = request.POST['user_id']
                user = User.objects.get(pk=user_id)
                user.is_seller = True
                user.seller_status = 'A'
                user.save()

            return HttpResponseRedirect(reverse('seller_manage'))
        return redirect('login')

    @classmethod
    def make_admin(cls, request):
        if request.user.is_authenticated:
            if request.method == 'POST':
                user_id = request.POST['user_id']
                user = User.objects.get(pk=user_id)
                user.is_admin = True
                user.save()

            return HttpResponseRedirect(reverse('manage_user'))
        return redirect('login')

    @classmethod
    def update_users_store_status(cls, request):
        user = get_object_or_404(User, username=request.user.username)

        if request.user.is_authenticated:
            if user.store_status == 'Aberto':
                user.store_status = 'Fechado'
                user.save()
                return redirect('home_seller')
            else:
                user.store_status = 'Aberto'
                user.save()
                redirect('home_seller')

        return redirect('home_seller')
class AddressView:
    @classmethod
    def create_address(cls, request):
        if request.user.is_authenticated:
            user = request.user
            form = AddressForm(request.POST or None)
            if request.method == 'POST':
                if form.is_valid():
                    address = form.save()
                    address.user = user
                    address.save()
                    return redirect('list_customer_address')
            return render(request, '../templates/address/create_address.html', {'form': form})
        return redirect('login')

    @classmethod
    def list_address(cls, request):
        if request.user.is_authenticated:
            user = request.user
            queried_user = get_object_or_404(User, username=user)
            addresses = Address.objects.filter(user=queried_user)

            return render(request, '../templates/address/list_address.html', {'addresses': addresses})
        return redirect('login')

    @classmethod
    def update_address(cls, request, address_id):
        address = get_object_or_404(Address, id=address_id)

        if request.user.is_authenticated:
            form = AddressForm(instance=address)
            user = request.user
            if request.method == 'POST':
                form = AddressForm(request.POST, instance=address)
                if form.is_valid():
                    address = form.save(commit=False)
                    address.user = user
                    address.save()

                    return redirect('list_customer_address')

            return render(request, '../templates/address/create_address.html', {
                'form': form,
                'post': address,
                'service_address': address
            })
        return redirect('login')

    @classmethod
    def delete_address(cls, request):
        if request.user.is_authenticated:
            if request.method == 'POST':
                address_id = request.POST['address_id']
                address = get_object_or_404(Address, id=address_id)
                user = get_object_or_404(User, username=address.user.username)

                address.delete()
                return redirect('list_customer_address')
        return redirect('login')

class ServiceAddressView:
    @classmethod
    def list_service_address(cls, request):
        if request.user.is_authenticated:
            user = request.user
            if user.id:
                service_address = ServiceAddress.objects.filter(user=user.id)
            else:
                service_address = ServiceAddress.objects.all()

            return render(request, 'service_address/home.html', {
                "services_address": service_address,
            })
        return redirect('login')

    @classmethod
    def create_service_address(cls, request):
        form = ServiceAddressForm()
        if request.user.is_authenticated:
            user = request.user
            if request.method == 'POST':
                form = ServiceAddressForm(request.POST or None)
                if form.is_valid():
                    service_address = form.save(commit=False)
                    service_address.user = user
                    service_address.save()

                    return redirect('list_service_address')

            return render(request, '../templates/service_address/create.html', {
                'form': form,
                'user_id': user
            })
        return redirect('login')

    @classmethod
    def update_service_address(cls, request, service_address_id):
        service_address = get_object_or_404(
            ServiceAddress, id=service_address_id)
        if request.user.is_authenticated:
            form = ServiceAddressForm(instance=service_address)
            user = request.user
            if request.method == 'POST':
                form = ServiceAddressForm(
                    request.POST, instance=service_address)
                if form.is_valid():
                    service_address = form.save(commit=False)
                    service_address.user = user
                    service_address.save()

                    return redirect('list_service_address')

            return render(request, '../templates/service_address/create.html', {
                'form': form,
                'post': service_address,
                'service_address': service_address
            })
        return redirect('login')

    @classmethod
    def delete_service_address(cls, request):
        if request.user.is_authenticated:
            if request.method == 'POST':
                service_address_id = request.POST['service_address_id']
                service_address = get_object_or_404(
                    ServiceAddress, id=service_address_id)

                service_address.delete()
                return redirect('list_service_address')
        return redirect('login')


class DeliveryTimeView:
    @classmethod
    def list_delivery_time(cls, request, service_address_id):
        if request.user.is_authenticated:
            if service_address_id:
                delivery_time = DeliveryTime.objects.filter(
                    service_address=service_address_id)
            else:
                delivery_time = DeliveryTime.objects.all()

            return render(request, '../templates/delivery_time/home.html', {
                "delivery_times": delivery_time,
                'service_address_id': service_address_id,
            })
        return redirect('login')

    @classmethod
    def create_delivery_time(cls, request, service_address_id):
        if request.user.is_authenticated:
            service_address = get_object_or_404(
                ServiceAddress, id=service_address_id)
            form = DeliveryTimeForm()

            if request.method == 'POST':
                form = DeliveryTimeForm(request.POST or None)
                if form.is_valid():
                    delivery_time = form.save(commit=False)
                    delivery_time.service_address = service_address
                    delivery_time.save()

                    return redirect('list_delivery_time', service_address_id=service_address_id)

            return render(request, '../templates/delivery_time/create.html', {
                'form': form,
                'service_address_id': service_address_id
            })
        return redirect('login')

    @classmethod
    def update_delivery_time(cls, request, delivery_time_id):
        if request.user.is_authenticated:
            delivery_time = get_object_or_404(
                DeliveryTime, id=delivery_time_id)
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
        return redirect('login')

    @classmethod
    def delete_delivery_time(cls, request):
        if request.user.is_authenticated:
            service_address_id = None

            if request.method == 'POST':
                delivery_time_id = request.POST.get('delivery_time_id')
                delivery_time = get_object_or_404(DeliveryTime, id=delivery_time_id)
                service_address_id = delivery_time.service_address.id

                delivery_time.delete()

            return redirect('list_delivery_time', service_address_id=service_address_id)
        return redirect('login')
