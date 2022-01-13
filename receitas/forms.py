from django import forms
from contas.models import Contas
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

class FiltrarReceitaForm(forms.Form):
    contas_opcoes = [
        ('', 'Selecione uma conta')
    ]
    for conta in Contas.objects.all().order_by('id'):
        contas_opcoes.append((conta.id, conta))


    valor_min = forms.FloatField(required=False, widget=forms.TextInput(attrs={"placeholder": "Valor mínimo"}))
    valor_max = forms.FloatField(required=False, widget=forms.TextInput(attrs={"placeholder": "Valor máximo"}))
    tipo = forms.ChoiceField(required=False, choices=Receitas.opcoes_tipo_receita, label="Tipo")
    descricao = forms.CharField(required=False, max_length=255, label="Descrição", widget=forms.TextInput(attrs={"placeholder": "Detalhes"}))
    conta = forms.ChoiceField(required=False, choices=contas_opcoes, label="Conta")
    data_recebimento_inicial = forms.CharField(required=False, max_length=255, widget=forms.TextInput(attrs={"placeholder": "DD/MM/AAAA"}))
    data_recebimento_final = forms.CharField(required=False, max_length=255, widget=forms.TextInput(attrs={"placeholder": "DD/MM/AAAA"}))
    data_esperado_inicial = forms.CharField(required=False, max_length=255, widget=forms.TextInput(attrs={"placeholder": "DD/MM/AAAA"}))
    data_esperado_final = forms.CharField(required=False, max_length=255, widget=forms.TextInput(attrs={"placeholder": "DD/MM/AAAA"}))