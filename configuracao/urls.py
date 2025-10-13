# urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
import configuracao.views as views

urlpatterns = [
    path('confg/', views.config, name='config'),
]