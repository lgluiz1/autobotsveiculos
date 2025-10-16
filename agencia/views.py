from django.shortcuts import render
from agencia.models import *
from configuracao.models import *
from django.core.paginator import Paginator
from django.http import JsonResponse
from configuracao.models import CarroMaisVisualizados
from mensagens.models import *
from django.db.models import F #
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from decimal import Decimal, InvalidOperation
from django.db import transaction

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
    
    # --- LÓGICA DE CONTAGEM AQUI ---
    obj, created = CarroMaisVisualizados.objects.get_or_create(carro=carro)
    obj.visualizacoes = F('visualizacoes') + 1
    obj.save(update_fields=['visualizacoes'])
    # --- FIM DA LÓGICA ---

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
    # Pega dados de Configuração dos endereços cadastrados podendo ser mais de 1
    enderecos = Endereco.objects.all()
    context = {
        'enderecos': enderecos
    }
    return render(request, 'paginas/pos_vendas.html', context)

def privacidade(request):
    return render(request, 'paginas/privacidades.html')
def duvidas(request):
    return render(request, 'paginas/duvidas.html')
def nossas_lojas(request):
    return render(request, 'paginas/nossas_lojas.html')

def sobre(request):
    return render(request, 'paginas/sobre.html')

def venda_seu_carro(request):
    return render(request, 'paginas/venda_seu_carro.html')

def financiamiento(request):
    return render(request, 'paginas/financiamento.html')

@require_POST
def enviar_proposta(request, carro_id):
    carro = get_object_or_404(Carro, id=carro_id)
    
    # Pega os dados do formulário
    nome = request.POST.get('nome')
    email = request.POST.get('email')
    telefone = request.POST.get('telefone')
    mensagem = request.POST.get('mensagem')

    # Validação simples (pode ser mais robusta com Django Forms)
    if not nome or not email or not telefone:
        return JsonResponse({'status': 'error', 'message': 'Nome, e-mail e telefone são obrigatórios.'}, status=400)

    # Cria e salva a proposta no banco de dados
    SolicitacaoDeProposta.objects.create(
        carro=carro,
        nome=nome,
        email=email,
        telefone=telefone,
        mensagem=mensagem
    )

    return JsonResponse({
        'status': 'success', 
        'message': 'Solicitação enviada! Um consultor vai entrar em contato com você.'
    })

@require_POST
def enviar_pos_vendas(request):
    # Pega os dados do formulário
    nome = request.POST.get('nome')
    cpf = request.POST.get('cpf')
    email = request.POST.get('email')
    telefone = request.POST.get('telefone')
    estado = request.POST.get('estado')
    cidade = request.POST.get('cidade')
    mensagem = request.POST.get('mensagem')
    como_nos_conheceu = request.POST.get('source') # Correct name from the form
    
    # --- CORREÇÃO AQUI ---
    loja_id = request.POST.get('loja') # This will be the ID (e.g., '1', '2')

    try:
        # Pega o objeto Endereco completo do banco de dados usando o ID
        endereco_obj = Endereco.objects.get(id=loja_id)
    except Endereco.DoesNotExist:
        # Se a loja não for encontrada, retorna um erro
        return JsonResponse({'status': 'error', 'message': 'Loja inválida selecionada.'}, status=400)

    # Cria e salva a solicitação no banco de dados
    PosVendas.objects.create(
        nome=nome,
        cpf=cpf,
        email=email,
        telefone=telefone,
        estado=estado,
        cidade=cidade,
        loja=endereco_obj, # Passa o objeto Endereco, não o ID
        como_nos_conheceu=como_nos_conheceu,
        mensagem=mensagem
    )

    return JsonResponse({
        'status': 'success', 
        'message': 'Solicitação enviada! Um consultor vai entrar em contato com você.'
    })

# Receber Financiamento
@require_POST
def solicitar_financiamento(request):
    try:
        # --- 1. COLETA DE DADOS DO FORMULÁRIO ---
        # Dados Pessoais
        nome = request.POST.get('nome', '').strip()
        email = request.POST.get('email', '').strip()
        cnh = request.POST.get('cnh', '').strip()
        telefone = request.POST.get('telefone', '').strip()
        celular = request.POST.get('celular', '').strip()
        cpf = request.POST.get('cpf', '').strip()
        estado_civil = request.POST.get('estado_civil')
        data_nascimento = request.POST.get('data_nascimento')

        # Dados Residenciais (note os nomes dos campos)
        endereco = request.POST.get('endereco', '').strip()
        numero = request.POST.get('numero', '').strip()
        bairro = request.POST.get('bairro', '').strip()
        cidade_res = request.POST.get('cidade_res', '').strip()
        uf_res = request.POST.get('uf_res')

        # Informações do Financiamento
        marca = request.POST.get('marca', '').strip()
        modelo = request.POST.get('modelo', '').strip()
        ano_fabricacao = request.POST.get('ano_fabricacao', '').strip()
        valor_entrada_str = request.POST.get('entrada', '0').strip()
        valor_financiar_str = request.POST.get('valor_financiar', '').strip()
        qtd_parcelas = request.POST.get('qtd_parcelas')
        observacao = request.POST.get('observacao', '').strip()

        # --- 2. VALIDAÇÃO BÁSICA ---
        if not all([nome, email, telefone, celular, cpf, data_nascimento, valor_financiar_str]):
            return JsonResponse({
                'status': 'error', 
                'message': 'Por favor, preencha todos os campos obrigatórios.'
            }, status=400)

        # --- 3. TRATAMENTO DE VALORES MONETÁRIOS ---
        # Remove "R$", pontos de milhar e substitui vírgula por ponto
        def limpar_valor(valor_str):
            if not valor_str:
                return Decimal('0.00')
            valor_limpo = valor_str.replace('R$', '').replace('.', '').replace(',', '.').strip()
            return Decimal(valor_limpo)

        valor_entrada_decimal = limpar_valor(valor_entrada_str)
        valor_financiar_decimal = limpar_valor(valor_financiar_str)
        
        # --- 4. SALVANDO NO BANCO DE DADOS ---
        FichaFinanciamento.objects.create(
            # Mapeando os campos do formulário para os campos do modelo
            nome_completo=nome,
            email=email,
            cnh=cnh,
            telefone=telefone,
            celular=celular,
            cpf=cpf,
            estado_civil=estado_civil,
            data_nascimento=data_nascimento,
            endereco=endereco,
            numero=numero,
            bairro=bairro,
            cidade=cidade_res, # Note a correspondência
            uf=uf_res,         # Note a correspondência
            marca_veiculo=marca,
            modelo_veiculo=modelo,
            ano_fabricacao=ano_fabricacao,
            valor_entrada=valor_entrada_decimal,
            valor_a_financiar=valor_financiar_decimal,
            qtd_parcelas=qtd_parcelas,
            observacao=observacao
        )

        # --- 5. RETORNO DE SUCESSO ---
        return JsonResponse({
            'status': 'success',
            'message': 'Sua ficha de financiamento foi enviada com sucesso! Em breve entraremos em contato.'
        }, status=201)

    except InvalidOperation:
        # Erro se o valor monetário for inválido (ex: "abc")
        return JsonResponse({
            'status': 'error',
            'message': 'Por favor, insira um valor monetário válido para entrada e valor a financiar.'
        }, status=400)
        
    except Exception as e:
        # Captura qualquer outro erro inesperado
        print(f"Erro inesperado: {e}") # Loga o erro no terminal para depuração
        return JsonResponse({
            'status': 'error',
            'message': 'Ocorreu um erro interno. Por favor, tente novamente mais tarde.'
        }, status=500)
    
@require_POST
@transaction.atomic # Garante que ou tudo é salvo, ou nada é salvo (proposta + fotos)
def enviar_proposta_venda(request):
    try:
        # Dados do Veículo
        marca = request.POST.get('marca')
        modelo = request.POST.get('modelo')
        versao = request.POST.get('versao')
        km = request.POST.get('quilometragem')
        ano = request.POST.get('ano')
        valor_str = request.POST.get('valor_desejado', '0').replace('.', '').replace(',', '.')

        # Dados Pessoais
        nome = request.POST.get('nome_proprietario')
        email = request.POST.get('email_proprietario')
        telefone = request.POST.get('telefone_proprietario')
        
        # Fotos (getlist é crucial para múltiplos arquivos)
        fotos = request.FILES.getlist('fotos')

        # Validação
        if not all([marca, modelo, versao, km, ano, valor_str, nome, email, telefone]):
            return JsonResponse({'message': 'Preencha todos os campos obrigatórios.'}, status=400)
        
        # Cria a proposta principal
        proposta = PropostaVenda.objects.create(
            marca=marca,
            modelo=modelo,
            versao=versao,
            quilometragem=int(km),
            ano=int(ano),
            valor_desejado=Decimal(valor_str),
            nome_proprietario=nome,
            email_proprietario=email,
            telefone_proprietario=telefone
        )

        # Salva as fotos, associando-as à proposta criada
        for f in fotos:
            FotoPropostaVenda.objects.create(proposta=proposta, imagem=f)

        return JsonResponse({
            'status': 'success',
            'message': 'Sua proposta foi enviada com sucesso! Em breve um de nossos consultores entrará em contato.'
        }, status=201)

    except Exception as e:
        # Loga o erro no terminal para depuração
        print(f"Erro ao processar proposta de venda: {e}")
        return JsonResponse({'message': 'Ocorreu um erro interno. Tente novamente.'}, status=500)