from django.db import models
from django.db.models.deletion import CASCADE
from contas.models import Contas

class Despesas(models.Model):

    opcoes_tipo_despesa = [
        ('AL', 'alimentação'),
        ('ED', 'educação'),
        ('LA', 'lazer'),
        ('MO', 'moradia'),
        ('RO', 'roupa'),
        ('SA', 'saúde'),
        ('TR', 'transporte'),
        ('OU', 'outros')
    ]

    valor = models.FloatField()
    dataRecebimento = models.DateField()
    dataRecebimentoEsperado = models.DateField()
    descricao = models.CharField(max_length=500, verbose_name='descrição')
    conta = models.ForeignKey(Contas, on_delete=CASCADE)
    tipoDespesa = models.CharField(max_length=2, choices=opcoes_tipo_despesa)