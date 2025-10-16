from django.db import models
from django.utils import timezone
from agencia.models import *


class PosVendas(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    estado = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    
    # Relação com a loja (está perfeito)
    loja = models.ForeignKey('configuracao.Endereco', on_delete=models.CASCADE)
    
    # Adicionado blank=True para tornar o campo opcional, como no formulário
    como_nos_conheceu = models.CharField(max_length=100, blank=True)
    
    mensagem = models.TextField()

    # Campo 'financiamento' foi removido para bater com o formulário.
    # Se precisar dele, lembre-se de adicioná-lo ao seu HTML e à sua view.

    # __str__ agora retorna o nome, que é mais útil no admin
    def __str__(self):
        return self.nome
    class Meta:
        verbose_name = 'Pos Venda'
        verbose_name_plural = 'Pos Vendas'
    
class SolicitacaoDeProposta(models.Model):
    carro = models.ForeignKey('agencia.Carro', on_delete=models.CASCADE)
    nome = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    telefone = models.CharField(max_length=20,null=True, blank=True)
    mensagem = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nome 
    
    class Meta:
        verbose_name = 'Solicitação de Proposta'
        verbose_name_plural = 'Solicitações de Propostas'

class FichaFinanciamento(models.Model):
    # --- DADOS PESSOAIS ---
    
    # Opções para o campo 'estado_civil'
    ESTADO_CIVIL_CHOICES = [
        ('solteiro', 'Solteiro(a)'),
        ('casado', 'Casado(a)'),
        ('divorciado', 'Divorciado(a)'),
        ('viuvo', 'Viúvo(a)'),
    ]

    # Opções para o status da solicitação
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('em_analise', 'Em Análise'),
        ('aprovado', 'Aprovado'),
        ('recusado', 'Recusado'),
    ]

    nome_completo = models.CharField(max_length=255)
    email = models.EmailField()
    cnh = models.CharField(max_length=20, blank=True, null=True, verbose_name="CNH")
    telefone = models.CharField(max_length=20)
    celular = models.CharField(max_length=20)
    cpf = models.CharField(max_length=14, verbose_name="CPF")
    estado_civil = models.CharField(max_length=15, choices=ESTADO_CIVIL_CHOICES)
    data_nascimento = models.DateField()

    # --- DADOS RESIDENCIAIS ---
    endereco = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    uf = models.CharField(max_length=2, verbose_name="UF")

    # --- INFORMAÇÕES DO FINANCIAMENTO ---
    
    # Opções para o campo 'qtd_parcelas'
    PARCELAS_CHOICES = [
        (12, '12x'),
        (24, '24x'),
        (36, '36x'),
        (48, '48x'),
        (60, '60x'),
    ]
    
    marca_veiculo = models.CharField(max_length=100, blank=True, null=True)
    modelo_veiculo = models.CharField(max_length=100, blank=True, null=True)
    ano_fabricacao = models.CharField(max_length=10, blank=True, null=True)
    
    # DecimalField é o ideal para valores monetários, evitando problemas de arredondamento.
    valor_entrada = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Valor da Entrada")
    valor_a_financiar = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor a Financiar")
    qtd_parcelas = models.IntegerField(choices=PARCELAS_CHOICES, verbose_name="Quantidade de Parcelas")
    
    observacao = models.TextField(blank=True, null=True, verbose_name="Observação")
    
    # --- CONTROLE INTERNO ---
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente', verbose_name="Status da Solicitação")
    data_solicitacao = models.DateTimeField(auto_now_add=True, verbose_name="Data da Solicitação")

    def __str__(self):
        # Isso ajuda a identificar cada ficha no painel de administração
        return f"Proposta de {self.nome_completo} ({self.cpf})"
    
    class Meta:
        verbose_name = "Ficha de Financiamento"
        verbose_name_plural = "Fichas de Financiamento"
        ordering = ['-data_solicitacao'] # Ordena as mais recentes primeiro no admin


# Modelo principal para a proposta de venda
class PropostaVenda(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('em_analise', 'Em Análise'),
        ('contatado', 'Contatado'),
        ('recusado', 'Recusado'),
    ]

    # Dados do Veículo
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    versao = models.CharField(max_length=100)
    quilometragem = models.PositiveIntegerField(verbose_name="Quilometragem (KM)")
    ano = models.PositiveIntegerField(verbose_name="Ano do Veículo")
    valor_desejado = models.DecimalField(max_digits=10, decimal_places=2)

    # Dados Pessoais
    nome_proprietario = models.CharField(max_length=255)
    email_proprietario = models.EmailField()
    telefone_proprietario = models.CharField(max_length=20)

    # Controle Interno
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    data_proposta = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Proposta de {self.nome_proprietario} para {self.marca} {self.modelo} ({self.ano})"

    class Meta:
        verbose_name = "Proposta de Venda"
        verbose_name_plural = "Propostas de Venda"
        ordering = ['-data_proposta']

# Modelo para armazenar as fotos de cada proposta
class FotoPropostaVenda(models.Model):
    proposta = models.ForeignKey(PropostaVenda, related_name='fotos', on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='propostas_venda/')

    def __str__(self):
        return f"Foto para a proposta de {self.proposta.nome_proprietario}"