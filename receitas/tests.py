from django.test import TestCase
from contas.models import Contas
from .models import Receitas


class TestModelsReceitas(TestCase):
    @classmethod
    def setUpTestData(cls):
        conta = Contas.objects.create(saldo=150.00, tipoConta='CC', instituicaoFinanceira='Teste')
        Receitas.objects.create(
            valor=50.00,
            dataRecebimento='2022-01-01',
            dataRecebimentoEsperado='2022-01-02',
            descricao="Teste",
            conta=conta,
            tipoReceita='OU'
        )

    def test_criar_Receita(self):
        receita = Receitas.objects.get(id=1)
        self.assertEqual(str(receita), 'Outros - R$ 50.00')

    def test_label_valor(self):
        Receita = Receitas.objects.get(id=1)
        field_label = Receita._meta.get_field('valor').verbose_name
        self.assertEqual(field_label, 'valor')

    def test_label_tipoReceita(self):
        Receita = Receitas.objects.get(id=1)
        field_label = Receita._meta.get_field('tipoReceita').verbose_name
        self.assertEqual(field_label, 'Tipo')

    def test_label_dataRecebimento(self):
        Receita = Receitas.objects.get(id=1)
        field_label = Receita._meta.get_field(
            'dataRecebimento').verbose_name
        self.assertEqual(field_label, 'Data recebimento')

    def test_label_dataRecebimentoEsperado(self):
        Receita = Receitas.objects.get(id=1)
        field_label = Receita._meta.get_field(
            'dataRecebimentoEsperado').verbose_name
        self.assertEqual(field_label, 'Data esperada para recebimento')
