# StudyFlow Django

Sistema web desenvolvido em Django para controle pessoal de estudos.

## Objetivo

O StudyFlow permite que cada usuário tenha acesso somente às próprias anotações, registre o tempo de estudo com um temporizador, defina uma meta diária e acompanhe seu histórico de progresso.

## Funcionalidades

* Cadastro, login e logout de usuários.
* Dashboard privado por usuário.
* Cadastro, edição e exclusão de anotações.
* Organização das anotações por matéria/categoria.
* Meta diária de estudo configurável no perfil.
* Temporizador de estudo com salvamento de sessão.
* Histórico agrupado por dia.
* Progresso da meta diária.
* Busca no histórico por data, matéria, título ou descrição da anotação.
* Cadastro de usuário bloqueando espaços e caracteres especiais no nome de usuário.
* Painel administrativo do Django.

## Tecnologias

* Python
* Django
* SQLite
* HTML
* CSS
* JavaScript

## Como rodar o projeto

### 1. Entrar na pasta do projeto

```bash
cd studyflow_django
```

### 2. Criar o ambiente virtual

```bash
python -m venv venv
```

### 3. Ativar o ambiente virtual

No PowerShell:

```bash
.\venv\Scripts\Activate.ps1
```

Se aparecer erro de permissão, rode:

```bash
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Depois tente ativar novamente:

```bash
.\venv\Scripts\Activate.ps1
```

No CMD:

```bash
venv\Scripts\activate.bat
```

### 4. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 5. Rodar as migrações

```bash
python manage.py migrate
```

### 6. Criar um usuário administrador opcional

```bash
python manage.py createsuperuser
```

### 7. Iniciar o servidor

```bash
python manage.py runserver
```

Acesse no navegador:

```text
http://127.0.0.1:8000/
```

## Regras do sistema

* Cada usuário visualiza somente suas próprias anotações.
* Cada usuário possui sua própria meta diária.
* As sessões de estudo salvas ficam vinculadas ao usuário logado.
* O nome de usuário aceita apenas letras, números e underline `_`.
* O sistema bloqueia cadastro de usuário com espaços ou caracteres especiais.

## Status

Projeto funcional com fluxo principal completo: usuário privado, anotações, meta diária, temporizador, histórico e busca.

## Melhorias recentes

* Busca no histórico por data, matéria, título ou descrição da anotação.
* Cadastro de usuário bloqueando espaços e caracteres especiais no nome de usuário.
* O nome de usuário agora aceita apenas letras, números e underline `_`.
