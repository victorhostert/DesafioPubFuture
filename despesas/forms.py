from django import forms
from .models import Despesas

class CriarDespesaForm(forms.ModelForm):
    required_css_class = 'obrigatorio'
    
    class Meta:
        model = Despesas
        fields = [
            'valor',
            'dataRecebimento',
            'dataRecebimentoEsperado',
            'tipoDespesa',
        ]
        widgets = {
            'dataRecebimento': forms.DateInput(attrs={'placeholder': 'DD/MM/AAAA'}, format="%d/%m/%Y"),
            'dataRecebimentoEsperado': forms.DateInput(attrs={'placeholder': 'DD/MM/AAAA'}, format="%d/%m/%Y")
        }

    def clean_valor(self):
        valor = self.cleaned_data.get('valor')
        conta = self.conta
        saldo = conta.saldo
        if valor > saldo:
            raise forms.ValidationError('O valor da despesa é superior ao saldo disponível')
        return valor