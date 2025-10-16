# seu_app/views.py
from django.http import JsonResponse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_POST # Garante que a view só aceite POST

# Importe seu modelo
from .models import Newsletter

@require_POST # Decorator que já trata requisições que não são POST, retornando erro 405.
def newsletter(request):
    name = request.POST.get('name', '').strip() # .strip() remove espaços em branco
    email = request.POST.get('email', '').strip()

    # 1. Validação de dados vazios
    if not name or not email:
        return JsonResponse({
            'status': 'error', 
            'message': 'Nome e e-mail são obrigatórios.'
        }, status=400) # Bad Request

    # 2. Validação do formato do e-mail
    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({
            'status': 'error', 
            'message': 'Por favor, insira um e-mail válido.'
        }, status=400) # Bad Request

    # 3. Verificação de duplicidade (como você já fazia)
    if Newsletter.objects.filter(email=email).exists():
        return JsonResponse({
            'status': 'error', 
            'message': 'Este e-mail já está cadastrado em nossa newsletter.'
        }, status=409) # Conflict

    # Se tudo estiver certo, cria o objeto
    Newsletter.objects.create(name=name, email=email)
    
    return JsonResponse({
        'status': 'success', 
        'message': 'Inscrição realizada com sucesso! Obrigado.'
    }, status=201) # Created