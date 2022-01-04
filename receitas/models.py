from django.db import models


class Receitas(models.Model):

    opcoes_tipo_receita = [
        'salário',
        'presente',
        'prêmio',
        'outros'
    ]

    valor = models.CharField(max_length=50)
    dataRecebimento = models.DateField()
    dataRecebimentoEsperado = models.DateField()
    descricao = models.CharField(max_length=500, verbose_name='descrição')
    conta = models.CharField(max_length=50)
    tipoReceita = models.CharField(max_length=50, choices=opcoes_tipo_receita)