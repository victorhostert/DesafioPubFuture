from django.urls import path
from . import views

app_name = 'receitas'

urlpatterns = [
    path('filtrar/', views.filtrar_receitas_view, name='filtrar'),
    path('cadastrar/<int:id>', views.cadastrar_receita_view, name='cadastrar'),
    path('<int:id>/', views.detalhe_receita_view, name='detalhe'),
    path('<int:id>/atualizar/', views.atualizar_receita_view, name='atualizar'),
    path('<int:id>/deletar/', views.deletar_receita_view, name='deletar'),
]
