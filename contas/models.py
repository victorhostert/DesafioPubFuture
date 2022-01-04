from django.db import models

class Contas(models.Model):

    opcoes_tipo_conta = [
        'alimentação',
        'educação',
        'lazer',
        'moradia',
        'roupa',
        'saúde',
        'transporte',
        'outros'
    ]

    saldo = models.CharField(max_length=50)
    tipoConta = models.CharField(max_length=50, choices=opcoes_tipo_conta)
    instituicaoFinanceira = models.CharField(max_length=255)