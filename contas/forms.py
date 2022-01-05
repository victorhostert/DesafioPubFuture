from django import forms
from django.shortcuts import get_object_or_404
from .models import Contas

class CriarContaForm(forms.ModelForm):
    class Meta:
        model = Contas
        fields = '__all__'


class TransferenciaForm(forms.Form):
    contas = tuple(Contas.objects.all())
    opcoes_contas = []
    for conta in contas:
        opcao = (conta.id, conta)
        opcoes_contas.append(opcao)

    conta1 = forms.ChoiceField(choices=opcoes_contas, label='Conta a ser debidata')
    conta2 = forms.ChoiceField(choices=opcoes_contas, label='Conta a ser creditada')
    valor = forms.FloatField(label='Valor a ser debitado')

    def clean_conta2(self):
        conta1 = self.cleaned_data.get('conta1')
        conta2 = self.cleaned_data.get('conta2')
        if conta1 == conta2:
            raise forms.ValidationError('As contas devem ser diferentes!')
        return conta2
    
    def clean_valor(self):
        conta1 = self.cleaned_data.get('conta1')
        conta = Contas.objects.get(id=conta1)
        valor = self.cleaned_data.get('valor')
        if conta.saldo < valor:
            raise forms.ValidationError('O saldo da conta a ser debitada é muito baixo para este valor!')
        return valor