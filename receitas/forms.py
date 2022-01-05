from django import forms
from .models import Receitas


class DateInput(forms.DateInput):
    input_type = 'date'

class CriarReceitaForm(forms.ModelForm):
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
            'dataRecebimento': DateInput(),
            'dataRecebimentoEsperado': DateInput()
        }
