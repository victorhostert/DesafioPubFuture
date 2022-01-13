from django import forms
from .models import Receitas


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
