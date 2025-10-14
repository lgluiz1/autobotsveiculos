from django.shortcuts import render
from agencia.models import *
from configuracao.models import *

def home(request):
    # pega todos os carros disponíveis
    carros = Carro.objects.filter(disponivel=True)
    marcas = Marca.objects.all()
    categorias = Categoria.objects.all()
    caracteristicas = Caracteristica.objects.all()

    contexto = {
        'carros': carros,
        'marcas': marcas,
        'categorias': categorias,
        'caracteristicas': caracteristicas
    }
    return render(request, 'home.html', contexto)


def detalhes(request, carro_id):
    carro = Carro.objects.get(id=carro_id)
    endereco = Endereco.objects.first()
    contatos = Contato.objects.first()

    context = {
        'carro': carro,
        'endereco': endereco,
        'contatos': contatos
    }

    return render(request, 'carros_detalhe.html', context)
