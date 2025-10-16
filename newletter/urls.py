# cria rota armazenamento newsletter
from django.urls import path
from .import views

urlpatterns = [
    path('newsletter/subscribe/', views.newsletter, name='newsletter_subscribe'),
]