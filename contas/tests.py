from django.test import TestCase
from django.urls import reverse
from contas.models import Contas
from .views import *
from .models import Contas


class TestModelsContas(TestCase):
    @classmethod
    def setUpTestData(cls):
        Contas.objects.create(saldo=150.00, tipoConta='CC',
                              instituicaoFinanceira='Teste')

    def test_criar_contas(self):
        conta = Contas.objects.get(id=1)
        self.assertEqual(str(conta), 'Teste - Conta Corrente')

    def test_label_saldo(self):
        conta = Contas.objects.get(id=1)
        field_label = conta._meta.get_field('saldo').verbose_name
        self.assertEqual(field_label, 'saldo')

    def test_label_tipoConta(self):
        conta = Contas.objects.get(id=1)
        field_label = conta._meta.get_field('tipoConta').verbose_name
        self.assertEqual(field_label, 'Tipo de Conta')

    def test_label_instituicaoFinanceira(self):
        conta = Contas.objects.get(id=1)
        field_label = conta._meta.get_field(
            'instituicaoFinanceira').verbose_name
        self.assertEqual(field_label, 'Instituição Financeira')


class TestViewsContas(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        numero_contas = 13
        for conta_id in range(numero_contas):
            Contas.objects.create(
                saldo=conta_id*10,
                tipoConta='OU',
                instituicaoFinanceira= f'Teste {conta_id}'
            )

    def test_detalhes_url_acessivel_por_nome(self):
        response = self.client.get(reverse('contas:detalhe', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 200)
        
    def test_detalhes_view_usa_template_correta(self):
        response = self.client.get(reverse('contas:detalhe', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'detalhe_conta.html')
