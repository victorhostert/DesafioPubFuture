from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from .models import Contas
from despesas.models import Despesas
from receitas.models import Receitas
from .forms import CriarContaForm, TransferenciaForm, FiltrarContaForm
from datetime import date

def paginator(request, object, number):
    paginator = Paginator(object, number)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except TypeError:
        page_obj = None
    return page_obj

def pesquisar_contas(request):
    contas = Contas.objects.all()    
    saldo_min = request.POST.get('saldo_min')
    saldo_max = request.POST.get('saldo_max')
    tipo_conta = request.POST.get('tipoConta')
    inst_financeira = request.POST.get('instituicaoFinanceira')
    resultado_filtro = None

    if saldo_min == '':
        saldo_min = 0
    if saldo_max == '':
        saldo_max = 9999999.99
    resultado_filtro = contas.filter(saldo__gte=saldo_min, saldo__lte=saldo_max)
    
    if tipo_conta and tipo_conta != '':
        resultado_filtro = contas.filter(tipoConta__iexact=tipo_conta)
    if inst_financeira and inst_financeira != '':
        resultado_filtro = contas.filter(instituicaoFinanceira__icontains=inst_financeira)

    return resultado_filtro

def detalhes_conta_view(request, id):
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

def atualizar_conta_view(request, id):
    conta = Contas.objects.get(id=id)
    if request.method == 'POST':
        form = CriarContaForm(request.POST, instance=conta)
        if form.is_valid():
            form.save()
            return redirect('homepage')
    else:
        form = CriarContaForm(instance=conta)
    context = {
        'form': form,
        'conta': conta
    }
    return render(request, 'atualizar_conta.html', context)

def deletar_conta_view(request, id):
    conta = Contas.objects.get(id=id)
    if request.method == "POST":
        conta.delete()
        return redirect('homepage')
    else:
        return render(request, 'deletar_conta.html', {'conta': conta})


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


def filtrar_contas_view(request):
    if request.method == 'POST':
        form = FiltrarContaForm(request.POST)
        contas = pesquisar_contas(request)
        return render(request, 'resultados_filtro_contas.html', {'form': form, 'contas': contas})
    else:
        form = FiltrarContaForm()
    return render(request, 'filtrar_contas.html', {'form': form})