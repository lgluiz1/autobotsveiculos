from django.contrib import admin
from agencia.models import *

class ImagemCarroInline(admin.TabularInline):
    model = ImagemCarro
    extra = 1  # mostra 1 campo vazio a mais (pode aumentar)

@admin.register(Carro)
class CarroAdmin(admin.ModelAdmin):
    inlines = [ImagemCarroInline]
    list_display = ('nome', 'ano', 'preco')
# Register your models here.
admin.site.register(Marca)
admin.site.register(Modelo)
admin.site.register(Categoria)
admin.site.register(Caracteristica)
admin.site.register(Opcional)
