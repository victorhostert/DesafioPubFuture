from django.shortcuts import redirect, render
from .forms import CriarReceitaForm
from contas.models import Contas

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