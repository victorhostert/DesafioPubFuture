from django.db import models

class Contas(models.Model):

    opcoes_tipo_conta = [
        ('CA', 'Carteira'),
        ('CC', 'Conta Corrente'),
        ('PO', 'Poupança')
    ]

    saldo = models.FloatField()
    tipoConta = models.CharField(max_length=2, choices=opcoes_tipo_conta, verbose_name='Tipo de Conta')
    instituicaoFinanceira = models.CharField(max_length=255, verbose_name='Instituição Financeira')

    def tipo_conta_descricao(self):
        if self.tipoConta == 'CA':
            return 'Carteira'
        if self.tipoConta == 'CC':
            return 'Conta Corrente'
        if self.tipoConta == 'PO':
            return 'Poupança'