from django.db import models

# Create your models here.

class Categoria(models.Model):
    titulo = models.CharField(max_length=150)
    
    def __str__(self):
        return self.titulo 

class Formulario(models.Model):
    titulo = models.CharField(max_length=100) 
    url = models.CharField(max_length=200)
    
class Assunto(models.Model):
    titulo = models.TextField() 
    resposta = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='Assuntos')
    
    def __str__(self):
        return self.titulo 
    