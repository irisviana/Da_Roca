import datetime
import json

from django.http import HttpResponse
from django.shortcuts import render,redirect,reverse
from django.contrib.auth import login, authenticate 
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm 
from .models import EnderecoAtendimento, Usuario, HorarioEntrega


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

class EnderecoAtendimentoView():
    @classmethod
    def cadastrarEnderecoAtendimento(self, request):
        mensagem = "" 
        if request.method == 'POST':
            cidade = request.POST['cidade']
            estado = request.POST['estado']
            usuarioId = request.POST['usuarioId']
            
            usuario = Usuario.objects.get(id = usuarioId)
            enderecoAtendimento = EnderecoAtendimento(cidade = cidade, estado = estado, usuario = usuario)
            enderecoAtendimento.save()
            mensagem = "Endereço de atendimento cadastrado com sucesso."
        
        return render(request, 'htmlListagemDoServiceAddress', { "mensagem" : mensagem })

    @classmethod
    def deleteEnderecoAtendimentoView(self, request):
        mensagem = ""
        if request.method == 'POST':
            enderecoAtendimentoId = request.POST['enderecoAtendimentoId']
            enderecoAtendimento = EnderecoAtendimento.objects.get(id = enderecoAtendimentoId)

            enderecoAtendimento.delete()
            mensagem = "Endereço de atendimento deletado com sucesso."

        return render(request, 'htmlListagemDoServiceAddress', { "mensage," : mensagem })

    @classmethod
    def atualizaEnderecoAtendimentoView(self, request):
        mensagem = ""
        if request.method == 'POST':
            cidade = request.POST['cidade']
            estado = request.POST['estado']
            enderecoAtendimentoId = request.POST['id']

            enderecoAtendimento = EnderecoAtendimento.objects.get(id = enderecoAtendimentoId)
            enderecoAtendimento.update(cidade = cidade, estado = estado)

            mensagem = "Endereço de atendimento atualizado com sucesso."

        return render(request, 'htmlListagemDoServiceAddress', { "mensagem" : mensagem })
    
class DeliveryTimeView():

    def lerHorarioEntrega(self, request):
        return render(request, 'usuario/horarioentrega/home.html')

    def criarHorarioEntrega(self, request):
        if request.method == 'POST':
            enderecoAtendimentoId = request.POST['enderecoAtendimentoId']
            hora = request.POST['hora']
            dia = request.POST['dia']

            enderecoAtendimento = EnderecoAtendimento.objects.get(id = enderecoAtendimentoId)

            horarioEntrega = HorarioEntrega(
                enderecoAtendimento = enderecoAtendimento, hora = hora, dia = dia)

            horarioEntrega.save()

            mensagem = 'Horário de entrega criado com sucesso.'
        
        return render(request, 'usuario/horarioentrega/home.html', {
            'mensagem': mensagem if mensagem else '',
        })

    def atualizerHorarioEntrega(self, request):
        if request.mothod == 'POST':
            horarioEntregaId = request.POST['horarioEntregaId']
            hora = request.POST.get('hora', None)
            dia = request.POST.get('dia', None)

            horarioEntrega = HorarioEntrega.objects.get(id = horarioEntregaId)

            horarioEntrega.update(
                hora = hora if hora else horarioEntrega.hora,
                dia = dia if dia else horarioEntrega.dia)

            mensagem = 'Horário de entrega atualizado com sucesso.'

        return render(request, 'usuario/horarioentrega/cadastro.html', {
            'mensagem': mensagem if mensagem else '',
        })

    def deletarHorarioEntrega(self, request):
        if request.mothod == 'POST':
            horarioEntregaId = request.POST['horarioEntregaId']
            hora = request.POST['hora']
            dia = request.POST['dia']

            horarioEntrega = HorarioEntrega.objects.get(id = horarioEntregaId)

            horarioEntrega.delete()

            mensagem = 'Horário de entrega removido com sucesso.'

        return render(request, 'usuario/horarioentrega/home.html', {
            'mensagem': mensagem if mensagem else '',
        })



