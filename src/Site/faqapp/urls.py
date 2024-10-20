from django.urls import path 
from . import views 

urlpatterns = [
    path("", views.index, name="index"), 
    path("categoria/<str:nome_categoria>", views.categoria, name = "categoria"),
    path("formulario/", views.formulario, name = "formulario"),
    path("teste", views.busca_categoria, name="busca_categoria")
]