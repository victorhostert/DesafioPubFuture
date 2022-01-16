from django.test import TestCase
from contas.models import Contas
from .models import Despesas


class TestModelsDespesas(TestCase):
    @classmethod
    def setUpTestData(cls):
        conta = Contas.objects.create(saldo=150.00, tipoConta='CC', instituicaoFinanceira='Teste')
        Despesas.objects.create(
            valor=50.00,
            dataPagamento='2022-01-01',
            dataPagamentoEsperado='2022-01-02',
            conta=conta,
            tipoDespesa='OU'
        )

    def test_criar_despesa(self):
        despesa = Despesas.objects.get(id=1)
        self.assertEqual(str(despesa), 'Outros - R$ 50.00')

    def test_label_valor(self):
        despesa = Despesas.objects.get(id=1)
        field_label = despesa._meta.get_field('valor').verbose_name
        self.assertEqual(field_label, 'valor')

    def test_label_tipoDespesa(self):
        despesa = Despesas.objects.get(id=1)
        field_label = despesa._meta.get_field('tipoDespesa').verbose_name
        self.assertEqual(field_label, 'Tipo')

    def test_label_dataPagamento(self):
        despesa = Despesas.objects.get(id=1)
        field_label = despesa._meta.get_field(
            'dataPagamento').verbose_name
        self.assertEqual(field_label, 'Data pagamento')

    def test_label_dataPagamentoEsperado(self):
        despesa = Despesas.objects.get(id=1)
        field_label = despesa._meta.get_field(
            'dataPagamentoEsperado').verbose_name
        self.assertEqual(field_label, 'Data pagamento esperado')


