from django.shortcuts import render
from agencia.models import *

def home(request):
    # pega todos os carros disponíveis
    carros = Carro.objects.filter(disponivel=True)

    contexto = {
        'carros': carros,
    }
    return render(request, 'home.html', contexto)
