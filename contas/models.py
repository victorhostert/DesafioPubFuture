from django.db import models


class Contas(models.Model):
    """
    Modelo para a tabela Contas

    Args:
        models (Model): Contém todos os campos essenciais e comportamentos dos dados armazenados
    """

    opcoes_tipo_conta = [
        ('', '--------'),
        ('CA', 'Carteira'),
        ('CC', 'Conta Corrente'),
        ('PO', 'Poupança')
    ]

    saldo = models.DecimalField(max_digits=15, decimal_places=2)
    tipoConta = models.CharField(
        max_length=2, choices=opcoes_tipo_conta, verbose_name='Tipo de Conta')
    instituicaoFinanceira = models.CharField(
        max_length=255, verbose_name='Instituição Financeira')

    def __str__(self) -> str:
        return f'{self.instituicaoFinanceira} - {self.get_tipoConta_display()}'