from django.urls import path
from . import views

app_name = 'receitas'

urlpatterns = [
    path('cadastrar/<int:id>', views.cadastrar_receita_view, name='cadastrar'),
]
