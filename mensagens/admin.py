from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(SolicitacaoDeProposta)
admin.site.register(PosVendas)
admin.site.register(PropostaVenda)

@admin.register(FichaFinanciamento)
class FichaFinanciamentoAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'cpf', 'status', 'data_solicitacao')
    list_filter = ('status', 'data_solicitacao')
    search_fields = ('nome_completo', 'cpf', 'email')


