# urls.py

from django.contrib import admin
from django.urls import path, include
from agencia import views

urlpatterns = [
    # urls.py
    path('get-modelos/', views.get_modelos_por_marca, name='get_modelos_por_marca'),
    path('get-modelos/<int:marca_id>/', views.get_modelos_por_marca_home, name='get_modelos_por_marca'),
    path('', views.home, name='home'),
    path('detalhes/<int:carro_id>', views.detalhes, name='detalhes'),
    path('pesquisa/', views.pesquisa, name='pesquisa'),
    path('pos-vendas/', views.pos_vendas, name='pos_vendas'),
    
]