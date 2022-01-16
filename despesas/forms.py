from django import forms
from django.db.utils import OperationalError
from contas.models import Contas
from .models import Despesas


class CriarDespesaForm(forms.ModelForm):
    """
    Formulário para criação de despesas

    Args:
        forms (ModelForm): Cria um formulário baseado em um model

    Raises:
        forms.ValidationError: Verifica se o valor da despesa é inferior ao saldo disponível
    """
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
    """
    Formulário para filtro de despesas, com todos os campos possíveis

    Args:
        forms (Form): Formulário padrão do Django Forms

    Raises:
        forms.ValidationError: Verifica se o valor máximo é superior ao valor mínimo
    """
    valor_min = forms.FloatField(required=False, widget=forms.TextInput(
        attrs={"placeholder": "Valor mínimo"}))
    valor_max = forms.FloatField(required=False, widget=forms.TextInput(
        attrs={"placeholder": "Valor máximo"}))
    tipo = forms.ChoiceField(
        required=False, choices=Despesas.opcoes_tipo_despesa, label="Tipo")
    conta = forms.ModelChoiceField(Contas.objects.all(), required=False)
    data_pagamento_inicial = forms.DateField(
        required=False, widget=forms.TextInput(attrs={"placeholder": "DD/MM/AAAA"}))
    data_pagamento_final = forms.DateField(
        required=False, widget=forms.TextInput(attrs={"placeholder": "DD/MM/AAAA"}))
    data_esperado_inicial = forms.DateField(
        required=False, widget=forms.TextInput(attrs={"placeholder": "DD/MM/AAAA"}))
    data_esperado_final = forms.DateField(
        required=False, widget=forms.TextInput(attrs={"placeholder": "DD/MM/AAAA"}))

    def clean_valor_max(self):
        valor_max = self.cleaned_data.get('valor_max')
        valor_min = self.cleaned_data.get('valor_min')
        if valor_max and valor_min:
            if valor_max < valor_min:
                raise forms.ValidationError(
                    'O valor máximo deve ser maior que o valor mínimo')
        return valor_max
