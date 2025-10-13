from django.db import models


# Marcas de carros
class Marca(models.Model):
    nome = models.CharField(max_length=100)
    img_upload = models.ImageField(upload_to='marcas/')

    def __str__(self):
        return self.nome
    
# Modelos de carros
class Modelo(models.Model):
    nome = models.CharField(max_length=100)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    img_upload = models.ImageField(upload_to='modelos/')

    def __str__(self):
        return f"{self.marca.nome} {self.nome}"

# Categorias de carros
class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome
    
# Características dos carros
class Caracteristica(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome
    

#Opcionais dos carros
class Opcional(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome
    
# Carros
class Carro(models.Model):
    nome = models.CharField(max_length=100)
    modelo = models.ForeignKey(Modelo, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    caracteristicas = models.ManyToManyField(Caracteristica, blank=True)
    opcionais = models.ManyToManyField(Opcional, blank=True)
    ano = models.CharField(max_length=100)
    cambio = models.CharField(max_length=100)
    combustivel = models.CharField(max_length=100)
    km = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    preco_ativo = models.BooleanField(default=True)    
    disponivel = models.BooleanField(default=True)
    informacoes = models.TextField(blank=True)

    # Carrega mmais de uma imagem
    img_upload = models.ImageField(upload_to='carros/')
    

    def __str__(self):
        return f"{self.modelo.marca.nome} {self.modelo.nome} - {self.ano}"