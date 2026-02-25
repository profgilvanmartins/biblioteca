from django.db import models
from datetime import date

class Autor(models.Model):
    nome = models.CharField(max_length=100)
    #retirei o campo idade
    
    def __str__(self):
        return self.nome
    
class Livro (models.Model):
    #atualização para "ManyToManyField" - permitir mais de um autor
    autores = models.ManyToManyField(Autor, related_name="livros", blank=True)
    titulo = models.CharField(max_length=200)
    resumo = models.TextField()
    data_pub = models.DateField()

    def __str__(self):
        return self.titulo