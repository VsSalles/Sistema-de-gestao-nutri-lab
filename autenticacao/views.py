from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from . utils import password_is_valid, email_html
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.conf import settings
import os
from . models import Ativacao
from hashlib import sha256


def cadastro(request):
    if request.user.is_authenticated:
        return redirect('/pacientes')
    elif request.method == 'GET':
        return render(request, 'cadastro.html')
    elif request.method == 'POST':
        usuario = request.POST.get('usuario')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if len(usuario.strip()) == 0 or len(email.strip()) == 0 or len(senha.strip()) == 0 or len(confirmar_senha.strip()) == 0:
            messages.add_message(request, messages.WARNING, 'todos os campos são obrigatorios!')
            return redirect('cadastro')
        
        if User.objects.filter(username=usuario).exists():
            messages.add_message(request, messages.INFO, 'ja existe alguem cadastrado com esse nome!')
            return redirect('cadastro')
        
        if not password_is_valid(request, senha, confirmar_senha):
            return redirect('cadastro')
        else:
            try:
                user = User.objects.create_user(username=usuario, email=email, password=senha, is_active=False)
                user.save()

                token = sha256(f'{usuario}{email}'.encode()).hexdigest()
                ativacao = Ativacao(token=token, user=user)
                ativacao.save()

                path_template = os.path.join(settings.BASE_DIR, 'autenticacao/templates/emails/cadastro_confirmado.html')
                email_html(path_template, 'Cadastro confirmado', [email,], username=usuario, link_ativacao=f"127.0.0.1:8000/auth/ativar_conta/{token}")

                messages.add_message(request, messages.SUCCESS, 'Cadastro realizado com sucesso, verique seu e-mail para ativar sua conta!')
                return redirect('login')
            except Exception as e:
                print(e)
                messages.add_message(request, messages.ERROR, 'Erro interno do sistema!')
                return redirect('cadastro')
            

def login(request):
    if request.user.is_authenticated:
        return redirect('/pacientes/')
    elif request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        usuario = request.POST.get('usuario')
        senha = request.POST.get('senha')

        user = auth.authenticate(request, username=usuario, password=senha)

        if not user:
            messages.add_message(request, messages.ERROR, 'Usuario ou senha invalido!')
            return redirect('login')
        else:
            auth.login(request,user)
            messages.add_message(request, messages.SUCCESS, 'Login realizado!')
            return redirect('/pacientes/')
        
def sair(request):
    auth.logout(request)
    return redirect('/auth/login')


def ativar_conta(request, token):
    token = get_object_or_404(Ativacao, token=token)
    if token.ativo:
        messages.add_message(request, messages.WARNING, 'Essa token já foi usado')
        return redirect('/auth/login')
    user = User.objects.get(username=token.user.username)
    user.is_active = True
    user.save()
    token.ativo = True
    token.save()
    messages.add_message(request, messages.SUCCESS, 'Conta ativa com sucesso')
    return redirect('/auth/login')