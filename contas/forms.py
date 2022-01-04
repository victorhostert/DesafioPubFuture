from django import forms
from .models import Contas

class CriarContaForm(forms.ModelForm):
    class Meta:
        model = Contas
        fields = '__all__'