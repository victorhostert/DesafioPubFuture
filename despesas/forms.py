from django import forms
from django.db.utils import OperationalError
from contas.models import Contas
from .models import Despesas


class CriarDespesaForm(forms.ModelForm):
    required_css_class = 'obrigatorio'

    class Meta:
        model = Despesas
        fields = [
            'valor',
            'dataPagamento',
            'dataPagamentoEsperado',
            'tipoDespesa',
        ]
        widgets = {
            'dataPagamento': forms.DateInput(attrs={'placeholder': 'DD/MM/AAAA'}, format="%d/%m/%Y"),
            'dataPagamentoEsperado': forms.DateInput(attrs={'placeholder': 'DD/MM/AAAA'}, format="%d/%m/%Y")
        }

    def clean_valor(self):
        valor = self.cleaned_data.get('valor')
        conta = self.conta
        saldo = conta.saldo
        if valor > saldo:
            raise forms.ValidationError(
                'O valor da despesa é superior ao saldo disponível')
        return valor


class FiltrarDespesaForm(forms.Form):
    contas_opcoes = [
        ('', 'Selecione uma conta')
    ]
    try:
        for conta in Contas.objects.all():
            contas_opcoes.append((conta.id, conta))
    except OperationalError:
        pass

    valor_min = forms.FloatField(required=False, widget=forms.TextInput(
        attrs={"placeholder": "Valor mínimo"}))
    valor_max = forms.FloatField(required=False, widget=forms.TextInput(
        attrs={"placeholder": "Valor máximo"}))
    tipo = forms.ChoiceField(
        required=False, choices=Despesas.opcoes_tipo_despesa, label="Tipo")
    conta = forms.ChoiceField(
        required=False, choices=contas_opcoes, label="Conta")
    data_pagamento_inicial = forms.DateField(
        required=False, max_length=255, widget=forms.TextInput(attrs={"placeholder": "DD/MM/AAAA"}))
    data_pagamento_final = forms.DateField(
        required=False, max_length=255, widget=forms.TextInput(attrs={"placeholder": "DD/MM/AAAA"}))
    data_esperado_inicial = forms.DateField(
        required=False, max_length=255, widget=forms.TextInput(attrs={"placeholder": "DD/MM/AAAA"}))
    data_esperado_final = forms.DateField(
        required=False, max_length=255, widget=forms.TextInput(attrs={"placeholder": "DD/MM/AAAA"}))
