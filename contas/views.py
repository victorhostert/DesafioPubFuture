from django.shortcuts import redirect, render
from .forms import CriarContaForm

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
