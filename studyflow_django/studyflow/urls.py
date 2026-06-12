from django.contrib import admin
from django.urls import path, include
from core import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('admin/', admin.site.urls),

    path('', include('usuarios.urls')),

    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),

    path(
        'criar-anotacao/',
        views.criar_anotacao,
        name='criar_anotacao'
    ),

    path(
        'editar-anotacao/<int:id>/',
        views.editar_anotacao,
        name='editar_anotacao'
    ),

    path(
        'excluir-anotacao/<int:id>/',
        views.excluir_anotacao,
        name='excluir_anotacao'
    ),

    path(
        'perfil/',
        views.perfil,
        name='perfil'
    ),

    path(
        'salvar-sessao/',
        views.salvar_sessao,
        name='salvar_sessao'
    ),

    path(
        'historico/',
        views.historico,
        name='historico'
    ),

]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )