from django.urls import path
from . import views

app_name = 'contas'

urlpatterns = [
    path('cadastrar/', views.criar_conta_view, name='cadastrar'),
]
