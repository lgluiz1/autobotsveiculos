# configuracao/context_processors.py
from .models import Logo  # ou o nome do seu model real

def site_config(request):
    logo = Logo.objects.first()
    return {
        'logo': logo,
    }
