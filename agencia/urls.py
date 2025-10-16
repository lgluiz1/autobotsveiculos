# urls.py

from django.contrib import admin
from django.urls import path, include
from agencia import views

urlpatterns = [
    # urls.py
    path('get-modelos/', views.get_modelos_por_marca, name='get_modelos_por_marca'),
    path('get-modelos/<int:marca_id>/', views.get_modelos_por_marca_home, name='get_modelos_por_marca'),
    path('carro/enviar-pos-vendas/', views.enviar_pos_vendas, name='enviar_pos_vendas'),
    path('financiamento/solicitar/', views.solicitar_financiamento, name='solicitar_financiamento'),
    path('vender-carro/enviar/', views.enviar_proposta_venda, name='enviar_proposta_venda'),
    path('carro/enviar-proposta/<int:carro_id>/', views.enviar_proposta, name='enviar_proposta'),
    path('', views.home, name='home'),
    path('detalhes/<int:carro_id>', views.detalhes, name='detalhes'),
    path('pesquisa/', views.pesquisa, name='pesquisa'),
    path('pos-vendas/', views.pos_vendas, name='pos_vendas'),
    path('privacidade/', views.privacidade, name='privacidade'),
    path('duvidas/', views.duvidas, name='duvidas'),
    path('nossas-lojas/', views.nossas_lojas, name='nossas_lojas'),
    path('venda-seu-carro/', views.venda_seu_carro, name='venda_seu_carro'),
    path('sobre/', views.sobre, name='sobre'),
    path('financiamiento/', views.financiamiento, name='financiamiento'),
    
]