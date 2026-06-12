from collections import defaultdict
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import PerfilForm
from .models import Anotacao, Categoria, Perfil, SessaoEstudo


def _formatar_horas(horas):
    total_minutos = int(round((horas or 0) * 60))
    h = total_minutos // 60
    m = total_minutos % 60

    if h and m:
        return f'{h}h{m:02d}'

    if h:
        return f'{h}h'

    return f'{m}min'


@login_required
def perfil(request):
    perfil, created = Perfil.objects.get_or_create(usuario=request.user)

    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=perfil)

        if form.is_valid():
            form.save()

            request.user.first_name = form.cleaned_data['first_name'].strip()
            request.user.last_name = form.cleaned_data['last_name'].strip()
            request.user.email = form.cleaned_data['email'].strip()
            request.user.save()

            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('perfil')
    else:
        form = PerfilForm(
            instance=perfil,
            initial={
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
            },
        )

    return render(request, 'Perfil.html', {'form': form, 'perfil': perfil})


@login_required
def dashboard(request):
    hoje = timezone.localdate()

    perfil, created = Perfil.objects.get_or_create(usuario=request.user)

    anotacoes = (
        Anotacao.objects.filter(usuario=request.user)
        .select_related('categoria')
        .order_by('-criada_em')
    )

    sessoes_hoje = SessaoEstudo.objects.filter(usuario=request.user, inicio__date=hoje)

    horas_hoje = sessoes_hoje.aggregate(total=Sum('horas'))['total'] or 0
    total_anotacoes = anotacoes.count()
    anotacoes_hoje = anotacoes.filter(criada_em__date=hoje).count()
    total_categorias = Categoria.objects.filter(usuario=request.user).count()
    meta_diaria = perfil.meta_diaria or 1
    progresso = min(int((horas_hoje / meta_diaria) * 100), 100) if meta_diaria else 0
    faltam = max(meta_diaria - horas_hoje, 0)

    return render(
        request,
        'Dashboard.html',
        {
            'anotacoes': anotacoes[:8],
            'perfil': perfil,
            'horas_hoje': horas_hoje,
            'horas_hoje_formatadas': _formatar_horas(horas_hoje),
            'faltam_formatadas': _formatar_horas(faltam),
            'total_anotacoes': total_anotacoes,
            'anotacoes_hoje': anotacoes_hoje,
            'total_categorias': total_categorias,
            'total_sessoes_hoje': sessoes_hoje.count(),
            'progresso': progresso,
            'faltam': faltam,
        },
    )


@login_required
def criar_anotacao(request):
    categorias = Categoria.objects.filter(usuario=request.user).order_by('nome')

    if request.method == 'POST':
        titulo = request.POST.get('titulo', '').strip()
        descricao = request.POST.get('descricao', '').strip()
        categoria_nome = request.POST.get('categoria', '').strip()

        if not titulo or not descricao:
            messages.error(request, 'Preencha o título e a descrição da anotação.')
            return redirect('criar_anotacao')

        categoria = None
        if categoria_nome:
            categoria, created = Categoria.objects.get_or_create(
                usuario=request.user,
                nome=categoria_nome,
            )

        Anotacao.objects.create(
            usuario=request.user,
            categoria=categoria,
            titulo=titulo,
            descricao=descricao,
        )

        messages.success(request, 'Anotação criada com sucesso!')
        return redirect('dashboard')

    return render(request, 'CriarAnotacao.html', {'categorias': categorias})


@login_required
def editar_anotacao(request, id):
    anotacao = get_object_or_404(Anotacao, id=id, usuario=request.user)
    categorias = Categoria.objects.filter(usuario=request.user).order_by('nome')

    if request.method == 'POST':
        titulo = request.POST.get('titulo', '').strip()
        descricao = request.POST.get('descricao', '').strip()
        categoria_nome = request.POST.get('categoria', '').strip()

        if not titulo or not descricao:
            messages.error(request, 'Preencha o título e a descrição da anotação.')
            return redirect('editar_anotacao', id=anotacao.id)

        categoria = None
        if categoria_nome:
            categoria, created = Categoria.objects.get_or_create(
                usuario=request.user,
                nome=categoria_nome,
            )

        anotacao.titulo = titulo
        anotacao.descricao = descricao
        anotacao.categoria = categoria
        anotacao.save()

        messages.success(request, 'Anotação atualizada com sucesso!')
        return redirect('dashboard')

    return render(
        request,
        'EditarAnotacao.html',
        {
            'anotacao': anotacao,
            'categorias': categorias,
        },
    )


@login_required
@require_POST
def excluir_anotacao(request, id):
    anotacao = get_object_or_404(Anotacao, id=id, usuario=request.user)
    anotacao.delete()
    messages.success(request, 'Anotação excluída com sucesso!')
    return redirect('dashboard')


@login_required
@require_POST
def salvar_sessao(request):
    try:
        segundos = int(request.POST.get('segundos', 0) or 0)
    except ValueError:
        return JsonResponse({'erro': 'Tempo inválido.'}, status=400)

    if segundos < 60:
        return JsonResponse({'erro': 'Estude pelo menos 1 minuto antes de salvar.'}, status=400)

    if segundos > 24 * 60 * 60:
        return JsonResponse({'erro': 'A sessão não pode passar de 24 horas.'}, status=400)

    fim = timezone.now()
    inicio = fim - timedelta(seconds=segundos)
    horas = segundos / 3600

    SessaoEstudo.objects.create(
        usuario=request.user,
        inicio=inicio,
        fim=fim,
        horas=horas,
    )

    return JsonResponse(
        {
            'mensagem': 'Sessão salva com sucesso!',
            'horas': round(horas, 2),
            'tempo_formatado': _formatar_horas(horas),
        }
    )


@login_required
def historico(request):
    perfil, created = Perfil.objects.get_or_create(usuario=request.user)
    busca = request.GET.get('q', '').strip()

    sessoes = SessaoEstudo.objects.filter(usuario=request.user).order_by('-inicio')
    anotacoes = (
        Anotacao.objects.filter(usuario=request.user)
        .select_related('categoria')
        .order_by('-criada_em')
    )

    if busca:
        anotacoes_encontradas = anotacoes.filter(
            Q(titulo__icontains=busca)
            | Q(descricao__icontains=busca)
            | Q(categoria__nome__icontains=busca)
            | Q(criada_em__date__icontains=busca)
        )

        sessoes_encontradas = sessoes.filter(
            Q(inicio__date__icontains=busca)
            | Q(fim__date__icontains=busca)
        )

        datas_encontradas = set()

        for anotacao in anotacoes_encontradas:
            datas_encontradas.add(timezone.localtime(anotacao.criada_em).date())

        for sessao in sessoes_encontradas:
            datas_encontradas.add(timezone.localtime(sessao.inicio).date())

        sessoes = [
            sessao for sessao in sessoes
            if timezone.localtime(sessao.inicio).date() in datas_encontradas
        ]
        anotacoes = [
            anotacao for anotacao in anotacoes
            if timezone.localtime(anotacao.criada_em).date() in datas_encontradas
        ]

    historico_por_data = defaultdict(lambda: {'sessoes': [], 'horas': 0, 'anotacoes': 0, 'anotacoes_lista': []})

    for sessao in sessoes:
        data = timezone.localtime(sessao.inicio).date()
        historico_por_data[data]['sessoes'].append(sessao)
        historico_por_data[data]['horas'] += sessao.horas or 0

    for anotacao in anotacoes:
        data = timezone.localtime(anotacao.criada_em).date()
        historico_por_data[data]['anotacoes'] += 1
        historico_por_data[data]['anotacoes_lista'].append(anotacao)

    dias = []
    for data, item in sorted(historico_por_data.items(), reverse=True):
        horas = item['horas']
        progresso = min(int((horas / perfil.meta_diaria) * 100), 100) if perfil.meta_diaria else 0
        dias.append(
            {
                'data': data,
                'sessoes': item['sessoes'],
                'horas': horas,
                'tempo_formatado': _formatar_horas(horas),
                'anotacoes': item['anotacoes'],
                'anotacoes_lista': item['anotacoes_lista'],
                'progresso': progresso,
                'meta_batida': horas >= perfil.meta_diaria,
            }
        )

    return render(
        request,
        'Historico.html',
        {
            'dias': dias,
            'perfil': perfil,
            'busca': busca,
        },
    )
