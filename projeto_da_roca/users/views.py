import datetime

from django.contrib import messages
from django.contrib.auth import login, authenticate,logout
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import ServiceAddress
from .models import User
from .models import DeliveryTime

# Create your views here.


def list_users(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)


def create_users(request):
    return render(request, '../templates/registration/create_costumer.html')


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
    return render(request, 'registration/login.html')





def home(request):
    return render(request, 'home.html')


# class ServiceAddressView:
#     @classmethod
#     def create_service_address(cls, request):
#         message = ""
#         if request.method == 'POST':
#             city = request.POST['cidade']
#             estado = request.POST['estado']
#             usuarioId = request.POST['usuarioId']
#
#             usuario = Usuario.objects.get(id = usuarioId)
#             enderecoAtendimento = EnderecoAtendimento(cidade=cidade, estado=estado, usuario=usuario)
#             enderecoAtendimento.save()
#             mensagem = "Endereço de atendimento cadastrado com sucesso."
#
#         return render(request, 'htmlListagemDoServiceAddress', {"mensagem": mensagem})
#
#     @classmethod
#     def deleteEnderecoAtendimentoView(self, request):
#         mensagem = ""
#         if request.method == 'POST':
#             enderecoAtendimentoId = request.POST['enderecoAtendimentoId']
#             enderecoAtendimento = EnderecoAtendimento.objects.get(id=enderecoAtendimentoId)
#
#             enderecoAtendimento.delete()
#             mensagem = "Endereço de atendimento deletado com sucesso."
#
#         return render(request, 'htmlListagemDoServiceAddress', {"mensage": mensagem})
#
#     @classmethod
#     def atualizaEnderecoAtendimentoView(cls, request):
#         mensagem = ""
#         if request.method == 'POST':
#             cidade = request.POST['cidade']
#             estado = request.POST['estado']
#             enderecoAtendimentoId = request.POST['id']
#
#             enderecoAtendimento = EnderecoAtendimento.objects.get(id = enderecoAtendimentoId)
#             enderecoAtendimento.update(cidade = cidade, estado = estado)
#
#             mensagem = "Endereço de atendimento atualizado com sucesso."
#
#         return render(request, 'htmlListagemDoServiceAddress', {"mensagem": mensagem})


class DeliveryTimeView:
    @classmethod
    def list_delivery_time(cls, request):
        delivery_time = DeliveryTime.objects.all()

        return render(request, '../templates/delivery_time/home.html', {
            "delivery_times": delivery_time,
        })

    @classmethod
    def create_delivery_time(cls, request):
        message = ''
        if request.method == 'POST':
            service_address_id = request.POST['enderecoAtendimentoId']
            time = request.POST['hora']
            day = request.POST['dia']

            service_address = ServiceAddress.objects.get(id=service_address_id)

            delivery_time = DeliveryTime(
                service_address=service_address, time=time, dia=day)

            delivery_time.save()

            message = 'Horário de entrega criado com sucesso.'
        
        return render(request, '../templates/delivery_time/create.html', {
            'message': message,
        })

    @classmethod
    def update_delivery_time(cls, request):
        message = ''
        if request.mothod == 'POST':
            delivery_time_id = request.POST['horarioEntregaId']
            time = request.POST.get('time', None)
            day = request.POST.get('day', None)

            delivery_time = DeliveryTime.objects.get(id=delivery_time_id)

            delivery_time.update(
                time=time if time else delivery_time.time,
                day=day if day else delivery_time.day)

            message = 'Horário de entrega atualizado com sucesso.'

        return render(request, 'usuario/delivery_time/create.html', {
            'mensagem': message,
        })

    @classmethod
    def delete_delivery_time(cls, request):
        message = ''
        if request.method == 'POST':
            delivery_time_id = request.POST['horarioEntregaId']

            try:
                delivery_time = DeliveryTime.objects.get(id=delivery_time_id)
                delivery_time.delete()

                message = 'Horário de entrega removido com sucesso.'
            except DeliveryTime.DoesNotExist as e:
                print(str(e))
                message = 'Horário de entrega não existe.'

            delivery_times = DeliveryTime.objects.all()

        return render(request, '../templates/delivery_time/home.html', {
            'message': message,
            'delivery_time': delivery_times,
        })
