# configuracao/context_processors.py
from .models import Logo, Favicon, Contato, RedeSocial   # ou o nome do seu model real

def site_config(request):
    logo = Logo.objects.first()
    favicon = Favicon.objects.first()
    contatos = Contato.objects.first()
    redesocial = RedeSocial.objects.first()
    # filtra todos os objetos da tabela RedeSocial

    return {
        'logo': logo,
        'favicon': favicon,
        'contatos': contatos,
        'redesocial': redesocial 
    }
