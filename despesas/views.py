from django.shortcuts import redirect, render
from despesas.models import Despesas
from .forms import CriarDespesaForm, FiltrarDespesaForm
from contas.models import Contas
from receitas.views import formatar_datas


def pesquisar_despesas(request):
    despesas = Despesas.objects.all().order_by('id')
    valor_min = request.POST.get('valor_min')
    valor_max = request.POST.get('valor_max')
    tipo = request.POST.get('tipo')
    conta = request.POST.get('conta')
    data_pagamento_inicial = request.POST.get('data_pagamento_inicial')
    data_pagamento_final = request.POST.get('data_pagamento_final')
    data_esperado_inicial = request.POST.get('data_esperado_inicial')
    data_esperado_final = request.POST.get('data_esperado_final')

    if not despesas:
        return None

    if conta == '':
        conta = Contas.objects.all()
    despesas = despesas.filter(conta__in=conta)

    if valor_min == '':
        valor_min = 0
    if valor_max == '':
        valor_max = 9999999.99
    despesas = despesas.filter(valor__gte=valor_min, valor__lte=valor_max)

    if tipo and tipo != '':
        despesas = despesas.filter(tipoDespesa__iexact=tipo)

    if data_pagamento_inicial and data_pagamento_inicial != '' and \
            data_pagamento_final and data_pagamento_final != '':
        data_pagamento_inicial = formatar_datas(data_pagamento_inicial)
        data_pagamento_final = formatar_datas(data_pagamento_final)
        despesas = despesas.filter(dataPagamento__range=[
                                   data_pagamento_inicial, data_pagamento_final])

    if data_esperado_inicial and data_esperado_inicial != '' and \
            data_esperado_final and data_esperado_final != '':
        data_esperado_inicial = formatar_datas(data_esperado_inicial)
        data_esperado_final = formatar_datas(data_esperado_final)
        despesas = despesas.filter(dataPagamentoEsperado__range=[
                                   data_esperado_inicial, data_esperado_final])

    if data_pagamento_inicial and data_pagamento_inicial != '':
        data_pagamento_inicial = formatar_datas(data_pagamento_inicial)
        despesas = despesas.filter(dataPagamento__gte=data_pagamento_inicial)

    if data_pagamento_final and data_pagamento_final != '':
        data_pagamento_final = formatar_datas(data_pagamento_final)
        despesas = despesas.filter(dataPagamento__lte=data_pagamento_final)

    if data_esperado_inicial and data_esperado_inicial != '':
        data_esperado_inicial = formatar_datas(data_esperado_inicial)
        despesas = despesas.filter(
            dataPagamentoEsperado__gte=data_esperado_inicial)

    if data_esperado_final and data_esperado_final != '':
        data_esperado_final = formatar_datas(data_esperado_final)
        despesas = despesas.filter(
            dataPagamentoEsperado__lte=data_esperado_final)

    return despesas


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
    if request.method == 'POST':
        conta = despesa.conta
        conta.saldo -= despesa.valor
        conta.save()
        despesa.delete()
        return redirect('contas:detalhes', id=conta.id)
    else:
        return render(request, 'deletar_despesa.html', {'despesa': despesa})


def filtrar_despesa_view(request):
    if request.method == 'POST':
        form = FiltrarDespesaForm(request.POST)
        if form.is_valid():
            despesas = pesquisar_despesas(request)
            return render(request, 'resultados_filtro_despesa.html', {'form': form, 'despesas': despesas})
    else:
        form = FiltrarDespesaForm()
    return render(request, 'filtrar_despesa.html', {'form': form})
