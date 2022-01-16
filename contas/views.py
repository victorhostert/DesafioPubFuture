from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from .models import Contas
from despesas.models import Despesas
from receitas.models import Receitas
from .forms import CriarContaForm, TransferenciaForm, FiltrarContaForm
from datetime import date


def paginator(request, object, number):
    """
    Função responsável por gerar a paginação nas views

    Args:
        request (HttpRequest): Uma requisição Http
        object (Model): Uma queryset de um Model
        number (Integer): Número de objetos por página

    Returns:
        QuerySet: Queryset dividido em vários setores, respectivos ao número de objetos por página (number)
    """
    paginator = Paginator(object, number)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except TypeError:
        page_obj = None
    return page_obj


def pesquisar_contas(request):
    """
    Filtra o model Contas retornando um queryset contendo o que passou nos filtros

    Args:
        request (HttpRequest): Requisição Http

    Returns:
        QuerySet: Contém o resultado dos filtros 
    """
    contas = Contas.objects.all().order_by('-id')
    saldo_min = request.POST.get('saldo_min')
    saldo_max = request.POST.get('saldo_max')
    tipo_conta = request.POST.get('tipoConta')
    inst_financeira = request.POST.get('instituicaoFinanceira')
    resultado_filtro = None

    if saldo_min == '':
        saldo_min = 0
    if saldo_max == '':
        saldo_max = 9999999.99
    resultado_filtro = contas.filter(
        saldo__gte=saldo_min, saldo__lte=saldo_max)

    if tipo_conta and tipo_conta != '':
        resultado_filtro = contas.filter(tipoConta__iexact=tipo_conta)
    if inst_financeira and inst_financeira != '':
        resultado_filtro = contas.filter(
            instituicaoFinanceira__icontains=inst_financeira)

    return resultado_filtro


def detalhes_conta_view(request, id):
    """
    Renderiza uma página contendo informações sobre uma conta, com suas despesas e receitas

    Args:
        request (HttpRequest): Requisição Http
        id (Integer): Número referente ao id da conta a ser exibida

    Returns:
        HttpResponse: Resposta Http contendo o contexto e uma página .html a ser renderizada
    """
    conta = Contas.objects.get(id=id)
    despesas = Despesas.objects.filter(conta=conta).order_by('dataPagamento')
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
    """
    Baseado no CriarContaForm, renderiza um formulário e salva as informações ao receber uma requisição POST

    Args:
        request (HttpRequest): Requisição Http

    Returns:
        HttpResponse: Resposta Http contendo o formulário e uma página .html a ser renderizada
    """
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
    """
    Atualiza uma Conta, capturando a instância através de um ID

    Args:
        request (HttpRequest): Requisição Http
        id (Integer): Número referente ao id da conta a ser atualizada

    Returns:
        HttpResponse: Resposta Http contendo o formulário e uma página .html a ser renderizada
    """
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
    """
    Deleta uma conta, após exigir mais uma confirmação

    Args:
        request (HttpRequest): Requisição Http
        id (Integer): Número referente ao id da conta a ser deletada

    Returns:
        HttpResponse: Resposta Http e a página .html a ser renderizada
    """
    conta = Contas.objects.get(id=id)
    if request.method == "POST":
        conta.delete()
        return redirect('homepage')
    else:
        return render(request, 'deletar_conta.html', {'conta': conta})


def transferencia_conta_view(request):
    """
    Transfere o saldo de uma conta a outra, contanto que as duas contas e o valor sejam lógicos

    Args:
        request (HttpRequest): Requisição Http

    Returns:
        HttpResponse: Resposta Http, formulário e a página .html a ser renderizada
    """
    if request.method == 'POST':
        form = TransferenciaForm(request.POST)
        if form.is_valid():
            conta_a_ser_debitada = form.cleaned_data['conta_a_ser_debitada']
            conta_a_ser_creditada = form.cleaned_data['conta_a_ser_creditada']
            valor = form.cleaned_data['valor']
            conta_a_ser_debitada.saldo = float(conta_a_ser_debitada.saldo)
            conta_a_ser_creditada.saldo = float(conta_a_ser_creditada.saldo)
            conta_a_ser_debitada.saldo -= valor
            conta_a_ser_creditada.saldo += valor
            Receitas.objects.create(
                dataRecebimento=date.today(),
                dataRecebimentoEsperado=date.today(),
                valor=valor,
                descricao=f'Transferência vinda de {conta_a_ser_debitada}',
                tipoReceita='OU',
                conta=conta_a_ser_creditada
            )
            Despesas.objects.create(
                dataPagamento=date.today(),
                dataPagamentoEsperado=date.today(),
                valor=valor,
                tipoDespesa='OU',
                conta=conta_a_ser_debitada
            )
            conta_a_ser_debitada.save()
            conta_a_ser_creditada.save()
            return redirect('homepage')
    else:
        form = TransferenciaForm()
    return render(request, 'transferencia.html', {'form': form})


def filtrar_contas_view(request):
    """
    Utiliza a função pesquisar_contas e o FiltrarContaForm para retornar um queryset,
    contendo os resultados do filtro

    Args:
        request (HttpRequest): Requisição Http

    Returns:
        HttpResponse: Resposta Http, formulário e a página .html a ser renderizada
    """
    if request.method == 'POST':
        form = FiltrarContaForm(request.POST)
        if form.is_valid():
            contas = pesquisar_contas(request)
            return render(request, 'resultados_filtro_contas.html', {'form': form, 'contas': contas})
    else:
        form = FiltrarContaForm()
    return render(request, 'filtrar_contas.html', {'form': form})
