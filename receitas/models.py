from django.db import models
from django.db.models.deletion import CASCADE
from contas.models import Contas


class Receitas(models.Model):

    opcoes_tipo_receita = [
        ('SA', 'Salário'),
        ('PS', 'Presente'),
        ('PM', 'Prêmio'),
        ('OU', 'Outros')
    ]

    valor = models.FloatField()
    dataRecebimento = models.DateField()
    dataRecebimentoEsperado = models.DateField()
    descricao = models.CharField(max_length=500, verbose_name='descrição')
    conta = models.ForeignKey(Contas, on_delete=CASCADE)
    tipoReceita = models.CharField(max_length=50, choices=opcoes_tipo_receita)