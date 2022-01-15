from django.urls import path
from . import views

app_name = 'contas'

urlpatterns = [
    path('cadastrar/', views.criar_conta_view, name='cadastrar'),
    path('transferir/', views.transferencia_conta_view, name='transferencia'),
    path('filtrar/', views.filtrar_contas_view, name='filtrar'),
    path('<int:id>/', views.detalhes_conta_view, name='detalhe'),
    path('<int:id>/atualizar', views.atualizar_conta_view, name='atualizar'),
    path('<int:id>/deletar', views.deletar_conta_view, name='deletar'),
]
