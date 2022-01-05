from django.shortcuts import redirect, render
from despesas.models import Despesas
from .forms import CriarDespesaForm
from contas.models import Contas


def cadastrar_despesa_view(request, id):
    conta = Contas.objects.get(id=id)
    if request.method == 'POST':
        form = CriarDespesaForm(request.POST)
        form.conta = conta
        if form.is_valid():
            instance = form.save(commit=False)
            instance.conta = conta
            conta.saldo -= instance.valor
            conta.save()
            instance.save()
            return redirect('contas:detalhes', id=id)
    else:
        form = CriarDespesaForm()

    return render(request, 'cadastrar_despesa.html', {'form': form, 'conta': conta})

def detalhe_despesa_view(request, id):
    despesa = Despesas.objects.get(id=id)
    return render(request, 'despesa_detalhe.html', {'despesa': despesa})

def atualizar_despesa_view(request, id):
    despesa = Despesas.objects.get(id=id)
    conta = despesa.conta
    if request.method == 'POST':
        conta.saldo += despesa.valor
        form = CriarDespesaForm(request.POST, instance=despesa)
        form.conta = conta
        if form.is_valid():
            conta.saldo -= form.cleaned_data['valor']
            conta.save()
            form.save()
            return redirect('despesas:detalhe', despesa.id)
    else:
        form = CriarDespesaForm(instance=despesa)

    return render(request, 'atualizar_despesa.html', {'form': form, 'conta': conta, 'despesa': despesa})

def deletar_despesa_view(request, id):
    despesa = Despesas.objects.get(id=id)
    conta = despesa.conta
    conta.saldo += despesa.valor
    conta.save()
    despesa.delete()
    return redirect('contas:detalhes', id=conta.id)