from django.shortcuts import redirect, render
from contas.models import Contas
from .forms import CriarReceitaForm
from .models import Receitas

def cadastrar_receita_view(request, id):
    conta = Contas.objects.get(id=id)
    if request.method == 'POST':
        form = CriarReceitaForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.conta = conta
            conta.saldo += instance.valor
            conta.save()
            instance.save()
            return redirect('contas:detalhes', id=id)
    else:
        form = CriarReceitaForm()

    return render(request, 'cadastrar_receita.html', {'form': form, 'conta': conta})

def detalhe_receita_view(request, id):
    receita = Receitas.objects.get(id=id)
    return render(request, 'receita_detalhe.html', {'receita': receita})