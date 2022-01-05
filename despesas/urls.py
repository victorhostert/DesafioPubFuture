from django.urls import path
from . import views

app_name = 'despesas'

urlpatterns = [
    path('cadastrar/<int:id>', views.cadastrar_despesa_view, name='cadastrar'),
]