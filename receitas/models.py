from django.db import models
from django.db.models.deletion import CASCADE
from contas.models import Contas


class Receitas(models.Model):
    """
    Modelo para a tabela Receitas

    Args:
        models (Model): Contém todos os campos essenciais e comportamentos dos dados armazenados
    """

    opcoes_tipo_receita = [
        ('', '--------'),
        ('SA', 'Salário'),
        ('PS', 'Presente'),
        ('PM', 'Prêmio'),
        ('OU', 'Outros')
    ]

    valor = models.DecimalField(max_digits=15, decimal_places=2)
    dataRecebimento = models.DateField(verbose_name='Data recebimento')
    dataRecebimentoEsperado = models.DateField(
        verbose_name='Data esperada para recebimento', null=True, blank=True)
    descricao = models.CharField(
        max_length=500, verbose_name='Descrição', null=True, blank=True)
    conta = models.ForeignKey(Contas, on_delete=CASCADE, default=None)
    tipoReceita = models.CharField(
        max_length=2, choices=opcoes_tipo_receita, verbose_name='Tipo')

    def __str__(self) -> str:
        return f'{self.get_tipoReceita_display()} - R$ {self.valor}'
