from django.db import models


class Contas(models.Model):

    opcoes_tipo_conta = [
        ('', '--------'),
        ('CA', 'Carteira'),
        ('CC', 'Conta Corrente'),
        ('PO', 'Poupança')
    ]

    saldo = models.FloatField()
    tipoConta = models.CharField(
        max_length=2, choices=opcoes_tipo_conta, verbose_name='Tipo de Conta')
    instituicaoFinanceira = models.CharField(
        max_length=255, verbose_name='Instituição Financeira')

    def __str__(self) -> str:
        return f'{self.instituicaoFinanceira} - {self.get_tipoConta_display()}'
