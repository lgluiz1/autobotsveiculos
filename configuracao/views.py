from django.shortcuts import render
from configuracao.models import *

# Create your views here.
def config(request):
    # puxa os dados do banco de dados
    logo = Logo.objects.first()

    context = {
        'logo': logo,
    }

    return render(request, 'base/base.html', context)