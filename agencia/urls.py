# urls.py

from django.contrib import admin
from django.urls import path, include
from agencia import views

urlpatterns = [
    path('', views.home, name='home'),
    path('detalhes/<int:carro_id>', views.detalhes, name='detalhes'),
    path('pesquisa/', views.pesquisa, name='pesquisa'),
]