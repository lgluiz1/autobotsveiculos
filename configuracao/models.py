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
    email = models.EmailField()

    def __str__(self):
        return f"Contato: {self.telefone} - {self.email}"
    
# Sobre a empresa
class Sobre(models.Model):
    descricao = models.TextField()
    img_upload = models.ImageField(upload_to='sobre/')

    def __str__(self):
        return "Sobre a Empresa"

# endereço da empresa
class Endereco(models.Model):
    rua = models.CharField(max_length=200)
    numero = models.CharField(max_length=20)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    cep = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.rua}, {self.cidade} - {self.estado}, {self.cep}"
    
