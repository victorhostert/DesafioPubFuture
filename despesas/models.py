from django.db import models
from django.db.models.deletion import CASCADE
from contas.models import Contas

class Despesas(models.Model):

    opcoes_tipo_despesa = [
        ('AL', 'Alimentação'),
        ('ED', 'Educação'),
        ('LA', 'Lazer'),
        ('MO', 'Moradia'),
        ('RO', 'Roupa'),
        ('SA', 'Saúde'),
        ('TR', 'Transporte'),
        ('OU', 'Outros')
    ]

    valor = models.FloatField()
    dataRecebimento = models.DateField(verbose_name='Data recebimento')
    dataRecebimentoEsperado = models.DateField(verbose_name='Data recebimento esperado')
    conta = models.ForeignKey(Contas, on_delete=CASCADE)
    tipoDespesa = models.CharField(max_length=2, choices=opcoes_tipo_despesa, verbose_name='Tipo')