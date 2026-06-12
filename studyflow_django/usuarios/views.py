import re

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('/dashboard/')

        messages.error(request, 'Usuário ou senha inválidos')

    return render(request, 'Login.html')


def cadastro_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        if not username or not password:
            messages.error(request, 'Informe usuário e senha para cadastrar.')
            return redirect('/cadastro/')

        if not re.fullmatch(r'[A-Za-z0-9_]+', username):
            messages.error(
                request,
                'O usuário deve conter apenas letras, números e underline (_). Não use espaços ou caracteres especiais.'
            )
            return redirect('/cadastro/')

        if len(username) < 3:
            messages.error(request, 'O usuário deve ter pelo menos 3 caracteres.')
            return redirect('/cadastro/')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Usuário já existe')
            return redirect('/cadastro/')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)
        messages.success(request, 'Cadastro realizado com sucesso!')

        return redirect('/dashboard/')

    return render(request, 'Registrar.html')


def logout_view(request):
    logout(request)
    return redirect('/login/')
