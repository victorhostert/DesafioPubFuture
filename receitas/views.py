from django.shortcuts import redirect, render
from contas.models import Contas
from .forms import CriarReceitaForm, FiltrarReceitaForm
from .models import Receitas


def formatar_datas(data):
    if '/' in data:
        dia = data[0:2]
        mes = data[3:5]
        ano = data[6:]
        data = f'{ano}-{mes}-{dia}'
    return data


def pesquisar_receitas(request):
    receitas = Receitas.objects.all().order_by('id')
    valor_min = request.POST.get('valor_min')
    valor_max = request.POST.get('valor_max')
    descricao = request.POST.get('descricao')
    tipo = request.POST.get('tipo')
    conta = request.POST.get('conta')
    data_recebimento_inicial = request.POST.get('data_recebimento_inicial')
    data_recebimento_final = request.POST.get('data_recebimento_final')
    data_esperado_inicial = request.POST.get('data_esperado_inicial')
    data_esperado_final = request.POST.get('data_esperado_final')

    if not receitas:
        return None

    if conta == '':
        conta = Contas.objects.all()
    receitas = receitas.filter(conta__in=conta)

    if valor_min == '':
        valor_min = 0
    if valor_max == '':
        valor_max = 9999999.99
    receitas = receitas.filter(valor__gte=valor_min, valor__lte=valor_max)

    if tipo and tipo != '':
        receitas = receitas.filter(tipoReceita__iexact=tipo)

    if descricao and descricao != '':
        receitas = receitas.filter(descricao__icontains=descricao)

    if data_recebimento_inicial and data_recebimento_inicial != '' and \
            data_recebimento_final and data_recebimento_final != '':
        data_recebimento_inicial = formatar_datas(data_recebimento_inicial)
        data_recebimento_final = formatar_datas(data_recebimento_final)
        receitas = receitas.filter(dataRecebimento__range=[
                                   data_recebimento_inicial, data_recebimento_final])

    if data_esperado_inicial and data_esperado_inicial != '' and \
            data_esperado_final and data_esperado_final != '':
        data_esperado_inicial = formatar_datas(data_esperado_inicial)
        data_esperado_final = formatar_datas(data_esperado_final)
        receitas = receitas.filter(dataRecebimentoEsperado__range=[
                                   data_esperado_inicial, data_esperado_final])

    if data_recebimento_inicial and data_recebimento_inicial != '':
        data_recebimento_inicial = formatar_datas(data_recebimento_inicial)
        receitas = receitas.filter(
            dataRecebimento__gte=data_recebimento_inicial)

    if data_recebimento_final and data_recebimento_final != '':
        data_recebimento_final = formatar_datas(data_recebimento_final)
        receitas = receitas.filter(dataRecebimento__lte=data_recebimento_final)

    if data_esperado_inicial and data_esperado_inicial != '':
        data_esperado_inicial = formatar_datas(data_esperado_inicial)
        receitas = receitas.filter(
            dataRecebimentoEsperado__gte=data_esperado_inicial)

    if data_esperado_final and data_esperado_final != '':
        data_esperado_final = formatar_datas(data_esperado_final)
        receitas = receitas.filter(
            dataRecebimentoEsperado__lte=data_esperado_final)

    return receitas


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


def atualizar_receita_view(request, id):
    receita = Receitas.objects.get(id=id)
    conta = receita.conta
    if request.method == 'POST':
        conta.saldo -= receita.valor
        form = CriarReceitaForm(request.POST, instance=receita)
        form.conta = conta
        if form.is_valid():
            conta.saldo -= form.cleaned_data['valor']
            conta.save()
            form.save()
            return redirect('receitas:detalhe', receita.id)
    else:
        form = CriarReceitaForm(instance=receita)

    return render(request, 'atualizar_receita.html', {'form': form, 'conta': conta, 'receita': receita})


def deletar_receita_view(request, id):
    receita = Receitas.objects.get(id=id)
    if request.method == 'POST':
        conta = receita.conta
        conta.saldo -= receita.valor
        conta.save()
        receita.delete()
        return redirect('contas:detalhes', id=conta.id)
    else:
        return render(request, 'deletar_receita.html', {'receita': receita})


def filtrar_receitas_view(request):
    if request.method == 'POST':
        form = FiltrarReceitaForm(request.POST)
        receitas = pesquisar_receitas(request)
        return render(request, 'resultados_filtro_receitas.html', {'form': form, 'receitas': receitas})
    else:
        form = FiltrarReceitaForm()
    return render(request, 'filtrar_receitas.html', {'form': form})
