from django.urls import path
from . import views

app_name = 'despesas'

urlpatterns = [
    path('cadastrar/<int:id>', views.cadastrar_despesa_view, name='cadastrar'),
    path('filtrar/', views.filtrar_despesa_view, name='filtrar'),
    path('<int:id>/', views.detalhe_despesa_view, name='detalhe'),
    path('<int:id>/atualizar/', views.atualizar_despesa_view, name='atualizar'),
    path('<int:id>/deletar/', views.deletar_despesa_view, name='deletar'),
]