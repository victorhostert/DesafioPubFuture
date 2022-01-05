from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from .models import Contas
from despesas.models import Despesas
from receitas.models import Receitas
from .forms import CriarContaForm, TransferenciaForm
from datetime import date

def paginator(request, object, number):
    paginator = Paginator(object, number)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except TypeError:
        page_obj = None
    return page_obj


def detalhes_view(request, id):
    conta = Contas.objects.get(id=id)
    despesas = Despesas.objects.filter(conta=conta).order_by('dataRecebimento')
    receitas = Receitas.objects.filter(conta=conta).order_by('dataRecebimento')
    pag_despesas = paginator(request, despesas, 10)
    pag_receitas = paginator(request, receitas, 10)
    context = {
        'conta': conta,
        'despesas': pag_despesas,
        'receitas': pag_receitas,
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

def transferencia_conta_view(request):
    if request.method == 'POST':
        form = TransferenciaForm(request.POST)
        if form.is_valid():
            conta1_id = form.cleaned_data['conta1']
            conta1 = get_object_or_404(Contas, id=conta1_id)
            conta2_id = form.cleaned_data['conta2']
            conta2 = get_object_or_404(Contas, id=conta2_id)
            valor = form.cleaned_data['valor']
            conta1.saldo -= valor
            conta2.saldo += valor
            Receitas.objects.create(
                dataRecebimento=date.today(),
                dataRecebimentoEsperado=date.today(),
                valor = valor,
                descricao = f'Transferência vinda de {conta1}',
                tipoReceita = 'OU',
                conta=conta2
            )
            Despesas.objects.create(
                dataRecebimento=date.today(),
                dataRecebimentoEsperado=date.today(),
                valor = valor,
                tipoDespesa = 'OU',
                conta=conta1
            )
            conta1.save()
            conta2.save()
            return redirect('homepage')
    else:
        form = TransferenciaForm()
    return render(request, 'transferencia.html', {'form': form})
