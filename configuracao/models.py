from django.db import models
from agencia.models import *

# Logo da empresa
class Logo(models.Model):
    img_upload = models.ImageField(upload_to='logo/')

    def __str__(self):
        return "Logo da Empresa"

class Favicon(models.Model):
    icon = models.ImageField(upload_to='favicon/', null=True, blank=True)
    favicon32 = models.ImageField(upload_to='favicon/', null=True, blank=True)
    favicon16 = models.ImageField(upload_to='favicon/', null=True, blank=True)
    favicon180 = models.ImageField(upload_to='favicon/', null=True, blank=True)

    def __str__(self):
        return "Favicon da Empresa"
class Video(models.Model):
    video = models.FileField(upload_to='video/', null=True, blank=True)

    def __str__(self):
        return "Video da Empresa"
# Menu de navegação
class Menu(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome
    
# Redes sociais
class RedeSocial(models.Model):    
    instagram = models.CharField(max_length=200, null=True, blank=True)
    facebook = models.CharField(max_length=200, null=True, blank=True)
    x = models.CharField(max_length=200, null=True, blank=True)
    youtube = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.instagram 

# Informações de contato
class Contato(models.Model):
    telefone = models.CharField(max_length=20)
    telefone2 = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return f"Contato: {self.telefone} - {self.email}"
    
# Sobre a empresa
class Sobre(models.Model):
    descricao = models.TextField()
    img_upload = models.ImageField(upload_to='sobre/',null=True, blank=True)

    def __str__(self):
        return "Sobre a Empresa"

# endereço da empresa
class Endereco(models.Model):
    nome_loja = models.CharField(max_length=100,null=True, blank=True)
    rua = models.CharField(max_length=200,null=True, blank=True)
    numero = models.CharField(max_length=20,null=True, blank=True)
    bairro = models.CharField(max_length=100,null=True, blank=True)
    cidade = models.CharField(max_length=100,null=True, blank=True)
    estado = models.CharField(max_length=100,null=True, blank=True)
    cep = models.CharField(max_length=20,null=True, blank=True)
    foto_loja = models.ImageField(upload_to='lojas_img/',null=True, blank=True)

    def __str__(self):
        return f"{self.rua}, {self.cidade} - {self.estado}, {self.cep}"
    

# emails
class emails(models.Model):
    email_newletter = models.EmailField(null=True, blank=True)
    email_contato = models.EmailField(null=True, blank=True)
    email_duvidas = models.EmailField(null=True, blank=True)
    email_pos_venda = models.EmailField(null=True, blank=True)
    email_marketing = models.EmailField(null=True, blank=True)

    email_para_enviar_newletter = models.EmailField(null=True, blank=True)
    email_para_enviar_contato = models.EmailField(null=True, blank=True)
    email_para_enviar_duvidas = models.EmailField(null=True, blank=True)
    email_para_enviar_pos_venda = models.EmailField(null=True, blank=True)
    email_para_enviar_marketing = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.email_contato
    
    class Meta:
        verbose_name = 'Emails'
        verbose_name_plural = 'Emails'

class CarroMaisVisualizados(models.Model):
    carro = models.ForeignKey('agencia.Carro', on_delete=models.CASCADE)
    visualizacoes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.carro} - Visualizações: {self.visualizacoes}"
    
    class Meta:
        verbose_name = 'Carro Mais Visualizados'
        verbose_name_plural = 'Carros Mais Visualizados'