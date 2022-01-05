from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from .models import Contas
from despesas.models import Despesas
from receitas.models import Receitas
from .forms import CriarContaForm

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
    despesas = Despesas.objects.filter(conta=conta)
    receitas = Receitas.objects.filter(conta=conta)
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
