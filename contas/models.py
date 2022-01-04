from django.db import models

class Contas(models.Model):

    opcoes_tipo_conta = [
        ('CA', 'carteira'),
        ('CC', 'conta corrente'),
        ('PO', 'poupança')
    ]

    saldo = models.CharField(max_length=50)
    tipoConta = models.CharField(max_length=2, choices=opcoes_tipo_conta)
    instituicaoFinanceira = models.CharField(max_length=255)