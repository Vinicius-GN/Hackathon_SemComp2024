from django.shortcuts import render
from .models import Categoria, Assunto, Formulario
# Create your views here.

def index(request):
    return  render(request, "faqapp/index.html", {
        "categorias": Categoria.objects.all()
    })

def formulario(request):
    formulario = Formulario.objects.all()
    return render(request, 'faqapp/formulario.html', {
        "formularios" : formulario
    })

def categoria(request, nome_categoria): 
    cat = Categoria.objects.filter(titulo=nome_categoria)[0]
    assuntos = Assunto.objects.filter(categoria = cat).all()
    return render(request, "faqapp/categoria.html", {
        "categoria": cat,
        "assuntos": assuntos 
    })

def busca_categoria(request):
    nome = request.GET.get('q')
    if nome:
        cat = Categoria.objects.filter(titulo__icontains=nome)
    else:
        cat = Categoria.objects.all()
    
    return  render(request, "faqapp/index.html", {
        "categorias": cat
    })
    
    
    
