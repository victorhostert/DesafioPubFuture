from django.db import models

class Contas(models.Model):

    opcoes_tipo_conta = [
        ('CA', 'Carteira'),
        ('CC', 'Conta Corrente'),
        ('PO', 'Poupança')
    ]

    saldo = models.FloatField()
    tipoConta = models.CharField(max_length=2, choices=opcoes_tipo_conta)
    instituicaoFinanceira = models.CharField(max_length=255)