from django.test import TestCase
from django.urls import reverse
from contas.models import Contas
from .models import Despesas


class TestModelsDespesas(TestCase):
    @classmethod
    def setUpTestData(cls):
        conta = Contas.objects.create(
            saldo=150.00, tipoConta='CC', instituicaoFinanceira='Teste')
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


class TestViewsDespesas(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        conta = Contas.objects.create(
            saldo=10000,
            tipoConta='OU',
            instituicaoFinanceira='Teste'
        )

        numero_despesas = 13
        for despesa_id in range(numero_despesas):
            Despesas.objects.create(
                valor=despesa_id*10,
                tipoDespesa='OU',
                dataPagamento='2022-01-01',
                dataPagamentoEsperado='2022-01-02',
                conta=conta,
            )

    def test_detalhes_url_acessivel_por_nome(self):
        response = self.client.get(
            reverse('despesas:detalhe', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 200)

    def test_detalhes_view_usa_template_correta(self):
        response = self.client.get(
            reverse('despesas:detalhe', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'detalhe_despesa.html')
