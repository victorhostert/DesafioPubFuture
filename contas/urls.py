from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar/', views.criar_conta_view, name='cadastro_conta'),
]
