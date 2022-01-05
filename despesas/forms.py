from django import forms
from .models import Despesas


class DateInput(forms.DateInput):
    input_type = 'date'

class CriarDespesaForm(forms.ModelForm):
    class Meta:
        model = Despesas
        fields = [
            'valor',
            'dataRecebimento',
            'dataRecebimentoEsperado',
            'tipoDespesa',
        ] 
        widgets = {
            'dataRecebimento': DateInput(),
            'dataRecebimentoEsperado': DateInput(),
        }