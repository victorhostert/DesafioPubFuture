from django.db import models

class Despesas(models.Model):

    opcoes_tipo_despesa = [
        'alimentação',
        'educação',
        'lazer',
        'moradia',
        'roupa',
        'saúde',
        'transporte',
        'outros'
    ]

    valor = models.CharField(max_length=50)
    dataRecebimento = models.DateField()
    dataRecebimentoEsperado = models.DateField()
    descricao = models.CharField(max_length=500, verbose_name='descrição')
    conta = models.CharField(max_length=50, primary_key=True)
    tipoDespesa = models.CharField(max_length=50, choices=opcoes_tipo_despesa)