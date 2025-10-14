from django.db import models

# Logo da empresa
class Logo(models.Model):
    img_upload = models.ImageField(upload_to='logo/')

    def __str__(self):
        return "Logo da Empresa"
    

# Menu de navegação
class Menu(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome
    
# Redes sociais
class RedeSocial(models.Model):
    nome = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return self.nome

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
    rua = models.CharField(max_length=200,null=True, blank=True)
    numero = models.CharField(max_length=20,null=True, blank=True)
    bairro = models.CharField(max_length=100,null=True, blank=True)
    cidade = models.CharField(max_length=100,null=True, blank=True)
    estado = models.CharField(max_length=100,null=True, blank=True)
    cep = models.CharField(max_length=20,null=True, blank=True)

    def __str__(self):
        return f"{self.rua}, {self.cidade} - {self.estado}, {self.cep}"
    
