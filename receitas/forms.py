from django import forms
from contas.models import Contas
from .models import Receitas
from django.db.utils import OperationalError


class CriarReceitaForm(forms.ModelForm):
    required_css_class = 'obrigatorio'

    class Meta:
        model = Receitas
        fields = [
            'valor',
            'dataRecebimento',
            'dataRecebimentoEsperado',
            'descricao',
            'tipoReceita'
        ]
        widgets = {
            'dataRecebimento': forms.DateInput(attrs={'placeholder': 'DD/MM/AAAA'}, format="%d/%m/%Y"),
            'dataRecebimentoEsperado': forms.DateInput(attrs={'placeholder': 'DD/MM/AAAA'}, format="%d/%m/%Y")
        }


class FiltrarReceitaForm(forms.Form):
    valor_min = forms.FloatField(required=False, widget=forms.TextInput(
        attrs={"placeholder": "Valor mínimo"}))
    valor_max = forms.FloatField(required=False, widget=forms.TextInput(
        attrs={"placeholder": "Valor máximo"}))
    tipo = forms.ChoiceField(
        required=False, choices=Receitas.opcoes_tipo_receita, label="Tipo")
    descricao = forms.CharField(required=False, max_length=255, label="Descrição",
                                widget=forms.TextInput(attrs={"placeholder": "Detalhes"}))
    conta = forms.ModelChoiceField(Contas.objects.all(), required=False)
    data_recebimento_inicial = forms.DateField(
        required=False, widget=forms.TextInput(attrs={"placeholder": "DD/MM/AAAA"}))
    data_recebimento_final = forms.DateField(
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
