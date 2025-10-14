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
    carros = Carro.objects.filter(disponivel=True)  # mostra só carros disponíveis

    # --- ORDENAÇÃO ---
    ordenar = request.GET.get('ordenar')
    if ordenar == 'maior_preco':
        carros = carros.order_by('-preco')
    elif ordenar == 'menor_preco':
        carros = carros.order_by('preco')
    elif ordenar == 'maior_ano':
        carros = carros.order_by('-ano')
    elif ordenar == 'menor_ano':
        carros = carros.order_by('ano')

    # --- MARCAS ---
    marcas = Marca.objects.all()
    marca_selecionada = request.GET.get('marca')

    # --- MODELOS ---
    modelos = Modelo.objects.all()
    modelo_selecionado = request.GET.get('modelo')


    # --- FILTROS ---
    marca = request.GET.get('marca')
    modelo = request.GET.get('modelo')
    ano = request.GET.get('ano')
    preco_min = request.GET.get('preco_min')
    preco_max = request.GET.get('preco_max')

    if marca and marca != 'Todos':
        carros = carros.filter(modelo__marca__nome__icontains=marca)
    if modelo and modelo != 'Todos':
        carros = carros.filter(modelo__nome__icontains=modelo)
    if ano and ano != 'Todos':
        carros = carros.filter(ano__icontains=ano)
    if preco_min:
        carros = carros.filter(preco__gte=preco_min)
    if preco_max:
        carros = carros.filter(preco__lte=preco_max)

    # --- PAGINAÇÃO ---
    page_number = request.GET.get('page', 1)
    paginator = Paginator(carros, 6)  # exibe 6 carros por "lote"
    page_obj = paginator.get_page(page_number)

    # --- AJAX (scroll infinito) ---
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = []
        for carro in page_obj:
            data.append({
                'id': carro.id,
                'nome': carro.nome,
                'marcas': marcas,
                'modelo': modelos,
                'ano': carro.ano,
                'preco': f'{carro.preco:,.2f}',
                'imagem': carro.imagem_principal.url if carro.imagem_principal else '',
                
            })
        return JsonResponse({'carros': data, 'has_next': page_obj.has_next()})

    return render(request, 'pagina_resultados.html', {'carros': page_obj})