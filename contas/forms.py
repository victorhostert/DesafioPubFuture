from django import forms
from django.db.models.fields import TextField
from django.db.utils import OperationalError
from .models import Contas


class CriarContaForm(forms.ModelForm):
    """
    Cria um formulário baseado no model Contas, com todos os campos

    Args:
        forms (ModelForm): Cria um formulário baseado em um model
    """
    required_css_class = 'obrigatorio'

    class Meta:
        model = Contas
        fields = '__all__'


class TransferenciaForm(forms.Form):
    """
    Cria o formulário para transferência de contas, também validando os dados

    Args:
        forms (Form): Formulário padrão do Django Forms

    Raises:
        forms.ValidationError: Verifica se as contas são diferentes
        forms.ValidationError: Verifica se a conta a ser debitada possui saldo suficiente

    Returns:
        attrs: retorna os atributos validados a serem consumidos na view
    """
    required_css_class = 'obrigatorio'

    conta_a_ser_debitada = forms.ModelChoiceField(Contas.objects.all())
    conta_a_ser_creditada = forms.ModelChoiceField(Contas.objects.all())
    valor = forms.FloatField(label='Valor a ser debitado')

    def clean_conta_a_ser_creditada(self):
        conta_a_ser_debitada = self.cleaned_data.get('conta_a_ser_debitada')
        conta_a_ser_creditada = self.cleaned_data.get('conta_a_ser_creditada')
        if conta_a_ser_debitada == conta_a_ser_creditada:
            raise forms.ValidationError('As contas devem ser diferentes!')
        return conta_a_ser_creditada

    def clean_valor(self):
        conta_a_ser_debitada = self.cleaned_data.get('conta_a_ser_debitada')
        valor = self.cleaned_data.get('valor')
        if conta_a_ser_debitada.saldo < valor:
            raise forms.ValidationError(
                'O saldo da conta a ser debitada é muito baixo para este valor!')
        return valor


class FiltrarContaForm(forms.Form):
    """
    Formulário para filtro de contas, com todos os campos possíveis

    Args:
        forms (Form): Formulário padrão do Django Forms

    Raises:
        forms.ValidationError: Verifica se o saldo máximo é superior ao saldo mínimo

    Returns:
        attrs: retorna os atributos validados a serem consumidos na view
    """
    saldo_min = forms.FloatField(required=False, widget=forms.TextInput(
        attrs={"placeholder": "Valor mínimo"}))
    saldo_max = forms.FloatField(required=False, widget=forms.TextInput(
        attrs={"placeholder": "Valor máximo"}))
    tipoConta = forms.ChoiceField(
        required=False, choices=Contas.opcoes_tipo_conta, label="Tipo da conta")
    instituicaoFinanceira = forms.CharField(required=False, max_length=255, label="Instituição Financeira", widget=forms.TextInput(
        attrs={"placeholder": "Digite seu banco"}))

    def clean_saldo_max(self):
        saldo_max = self.cleaned_data.get('saldo_max')
        saldo_min = self.cleaned_data.get('saldo_min')
        if saldo_max and saldo_min:
            if saldo_max < saldo_min:
                raise forms.ValidationError(
                    'O saldo máximo deve ser maior que o saldo mínimo')
        return saldo_max
