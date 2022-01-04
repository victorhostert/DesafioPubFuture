from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='homepage'),
    path('contas/', include('contas.urls')),
    path('despesas/', include('despesas.urls')),
    path('receitas/', include('receitas.urls')),
]
