from django.shortcuts import redirect, render
from contas.models import Contas
from .forms import CriarReceitaForm, FiltrarReceitaForm
from .models import Receitas


def formatar_datas(data):
    """
    Recebe datas no formato dd/mm/YYYY
    e as retorna no formato YYYY-mm-dd

    Args:
        data (string): Datas conforme vindas do formulário

    Returns:
        string: Data formatada para YYYY-mm-dd
    """
    if '/' in data:
        dia = data[0:2]
        mes = data[3:5]
        ano = data[6:]
        data = f'{ano}-{mes}-{dia}'
    return data


def pesquisar_receitas(request):
    """
    Filtra o model Receitas retornando um queryset contendo o que passou nos filtros

    Args:
        request (HttpRequest): Requisição Http

    Returns:
        QuerySet: Contém o resultado dos filtros 
    """
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
    """
    Baseado no CriarReceitaForm, renderiza um formulário e salva as informações ao receber uma requisição POST

    Args:
        request (HttpRequest): Requisição Http

    Returns:
        HttpResponse: Resposta Http contendo o formulário e uma página .html a ser renderizada
    """
    conta = Contas.objects.get(id=id)
    if request.method == 'POST':
        form = CriarReceitaForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.conta = conta
            conta.saldo += instance.valor
            conta.save()
            instance.save()
            return redirect('contas:detalhe', id=id)
    else:
        form = CriarReceitaForm()

    return render(request, 'cadastrar_receita.html', {'form': form, 'conta': conta})


def detalhe_receita_view(request, id):
    """
    Renderiza uma página contendo informações sobre uma receitaa

    Args:
        request (HttpRequest): Requisição Http
        id (Integer): Número referente ao id da receita a ser exibida

    Returns:
        HttpResponse: Resposta Http contendo o contexto e uma página .html a ser renderizada
    """
    receita = Receitas.objects.get(id=id)
    return render(request, 'detalhe_receita.html', {'receita': receita})


def atualizar_receita_view(request, id):
    """
    Atualiza uma Receita, capturando a instância através de um ID

    Args:
        request (HttpRequest): Requisição Http
        id (Integer): Número referente ao id da despesa a ser atualizada

    Returns:
        HttpResponse: Resposta Http contendo o formulário e uma página .html a ser renderizada
    """
    receita = Receitas.objects.get(id=id)
    conta = receita.conta
    if request.method == 'POST':
        conta.saldo -= receita.valor
        form = CriarReceitaForm(request.POST, instance=receita)
        form.conta = conta
        if form.is_valid():
            conta.saldo += form.cleaned_data['valor']
            conta.save()
            form.save()
            return redirect('contas:detalhe', conta.id)
    else:
        form = CriarReceitaForm(instance=receita)

    return render(request, 'atualizar_receita.html', {'form': form, 'conta': conta, 'receita': receita})


def deletar_receita_view(request, id):
    """
    Deleta uma receita, após exigir mais uma confirmação

    Args:
        request (HttpRequest): Requisição Http
        id (Integer): Número referente ao id da receita a ser deletada

    Returns:
        HttpResponse: Resposta Http e a página .html a ser renderizada
    """
    receita = Receitas.objects.get(id=id)
    if request.method == 'POST':
        conta = receita.conta
        conta.saldo -= receita.valor
        conta.save()
        receita.delete()
        return redirect('contas:detalhe', id=conta.id)
    else:
        return render(request, 'deletar_receita.html', {'receita': receita})


def filtrar_receitas_view(request):
    """
    Utiliza a função pesquisar_receitas e o FiltrarReceitaForm para retornar um queryset,
    contendo os resultados do filtro

    Args:
        request (HttpRequest): Requisição Http

    Returns:
        HttpResponse: Resposta Http, formulário e a página .html a ser renderizada
    """
    if request.method == 'POST':
        form = FiltrarReceitaForm(request.POST)
        if form.is_valid():
            receitas = pesquisar_receitas(request)
            return render(request, 'resultados_filtro_receitas.html', {'form': form, 'receitas': receitas})
    else:
        form = FiltrarReceitaForm()
    return render(request, 'filtrar_receitas.html', {'form': form})
