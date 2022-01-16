from django.shortcuts import render
from contas.models import Contas
from contas.views import paginator


def homepage(request):
    """Renderiza uma template html a partir de uma HttpRequest, retornando uma HttpResponse,
    passando contas e o saldo total como contexto

    Args:
        request (HttpRequest): Uma requisição Http que contém metadata sobre a requisição

    Returns:
        HttpResponse: Uma resposta à requisição Http, contendo o contexto e arquivo html a ser renderizado
    """
    contas = Contas.objects.all()
    saldo_total = 0
    if contas:
        for conta in contas:
            saldo_total += conta.saldo
    else:
        contas = []

    contas = paginator(request, contas, 10)
    context = {
        'contas': contas,
        'saldo_total': saldo_total
    }
    return render(request, 'homepage.html', context)
