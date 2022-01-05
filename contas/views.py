from django.shortcuts import redirect, render
from .models import Contas
from despesas.models import Despesas
from receitas.models import Receitas
from .forms import CriarContaForm

def detalhes_view(request, id):
    conta = Contas.objects.get(id=id)
    despesas = Despesas.objects.filter(conta=conta)
    receitas = Receitas.objects.filter(conta=conta)
    context = {
        'conta': conta,
        'despesas': despesas,
        'receitas': receitas,
    }
    return render(request, 'detalhe_conta.html', context)

def criar_conta_view(request):
    if request.method == 'POST':
        form = CriarContaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('homepage')
    else:
        form = CriarContaForm()
    context = {
        'form': form,
    }
    return render(request, 'cadastro_conta.html', context)
