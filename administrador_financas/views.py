from django.shortcuts import render
from contas.models import Contas

def homepage(request):
    contas = Contas.objects.all()
    saldo_total = 0
    for conta in contas:
        saldo_total += conta.saldo
    context = {
        'contas': contas,
        'saldo_total': saldo_total
    }
    return render(request, 'homepage.html', context)