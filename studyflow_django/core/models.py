from django.db import models
from django.contrib.auth.models import User


class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    meta_diaria = models.IntegerField(default=4)

    def __str__(self):
        return f"Perfil de {self.usuario.username}"


class Categoria(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)

    class Meta:
        ordering = ['nome']
        constraints = [
            models.UniqueConstraint(fields=['usuario', 'nome'], name='categoria_unica_por_usuario')
        ]

    def __str__(self):
        return self.nome


class Anotacao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, null=True, blank=True, on_delete=models.SET_NULL)
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    criada_em = models.DateTimeField(auto_now_add=True)
    atualizada_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-criada_em']

    def __str__(self):
        return self.titulo


class SessaoEstudo(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    inicio = models.DateTimeField()
    fim = models.DateTimeField()
    horas = models.FloatField(default=0)

    class Meta:
        ordering = ['-inicio']

    @property
    def duracao_minutos(self):
        return round((self.horas or 0) * 60)

    def __str__(self):
        return f"{self.usuario.username} - {self.inicio:%d/%m/%Y %H:%M}"
