from django.shortcuts import render
from agencia.models import *
from configuracao.models import *
from django.core.paginator import Paginator
from django.http import JsonResponse

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

def pesquisa(request):
    carros = Carro.objects.all()

    marca = request.GET.get('marca')
    modelo = request.GET.get('modelo')
    ano = request.GET.get('ano')
    preco_min = request.GET.get('preco_min')
    preco_max = request.GET.get('preco_max')
    ordenar = request.GET.get('ordenar')

    if marca:
        carros = carros.filter(modelo__marca_id=marca)

    if modelo:
        carros = carros.filter(modelo__nome__icontains=modelo)

    if ano:
        carros = carros.filter(ano=ano)

    if preco_min:
        carros = carros.filter(preco__gte=preco_min)

    if preco_max:
        carros = carros.filter(preco__lte=preco_max)

    if ordenar == 'preco_asc':
        carros = carros.order_by('preco')
    elif ordenar == 'preco_desc':
        carros = carros.order_by('-preco')
    elif ordenar == 'ano_asc':
        carros = carros.order_by('ano')
    elif ordenar == 'ano_desc':
        carros = carros.order_by('-ano')

    context = {
        'carros': carros,
        'marcas': Marca.objects.all(),
        'modelos': Modelo.objects.all(),
        'anos': Carro.objects.values_list('ano', flat=True).distinct(),
    }
    return render(request, 'pagina_resultados.html', context)

def get_modelos_por_marca(request):
    marca_id = request.GET.get('marca_id')
    if not marca_id:
        return JsonResponse({'error': 'Marca ID não fornecida'}, status=400)
    modelos = Modelo.objects.filter(marca_id=marca_id).values('id', 'nome')
    return JsonResponse(list(modelos), safe=False)

def get_modelos_por_marca_home(request, marca_id):
    modelos = Modelo.objects.filter(marca_id=marca_id).values('id', 'nome')
    return JsonResponse(list(modelos), safe=False)

def pos_vendas(request):
    return render(request, 'paginas/pos_vendas.html')