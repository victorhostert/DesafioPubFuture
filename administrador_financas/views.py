from django.shortcuts import render
from contas.models import Contas

def homepage(request):
    contas = Contas.objects.all()
    context = {
        'contas': contas
    }
    return render(request, 'homepage.html', context)