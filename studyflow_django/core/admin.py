from django.contrib import admin

from .models import Anotacao, Categoria, Perfil, SessaoEstudo


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'meta_diaria')
    search_fields = ('usuario__username', 'usuario__email')


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'usuario')
    search_fields = ('nome', 'usuario__username')


@admin.register(Anotacao)
class AnotacaoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'usuario', 'categoria', 'criada_em', 'atualizada_em')
    list_filter = ('categoria', 'criada_em')
    search_fields = ('titulo', 'descricao', 'usuario__username')
    date_hierarchy = 'criada_em'


@admin.register(SessaoEstudo)
class SessaoEstudoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'inicio', 'fim', 'horas')
    list_filter = ('inicio',)
    search_fields = ('usuario__username',)
    date_hierarchy = 'inicio'
