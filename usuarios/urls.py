from django.urls import path
from usuarios.views import login, cadastro, logout
from . import views
urlpatterns = [

    path('cadastro', cadastro, name='cadastro'),
    path('logout', logout, name='logout'),
    path('buscar', views.buscar, name='buscar'),
    path('', views.login, name='index'),
]
