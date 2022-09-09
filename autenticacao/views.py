from pickle import TRUE
from django.shortcuts import render, redirect, get_object_or_404
from .utils import password_is_valid, email_html
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages, auth
from django.conf import settings
import os
from .models import Ativacao
from hashlib import sha256

#Função que é chamada ao acessar a url /cadastro
def cadastro(request):
    
    #Caso a requisição seja feita via url apenas renderizar as páginas
    if request.method == "GET":
        
        #Se o usuário já está autenticado, renderizar pagina principal
        if request.user.is_authenticated:
            return redirect('/pacientes/')

        return render(request, 'cadastro.html')
    
    #Caso a requisição seja POST, via formulário
    elif request.method == "POST":
        
        #Pega os dados do formulário
        username = request.POST.get('usuario')
        senha = request.POST.get('senha')
        email = request.POST.get('email')
        confirmar_senha = request.POST.get('confirmar_senha')
        
        #Filtragem do banco de dados para saber se já existe o nome cadastrado e enviar a respectiva mensagem
        usuario = User.objects.filter(username=username).first()
        if usuario: 
            messages.add_message(request, constants.WARNING, 'Este nome já está em uso!')
            return redirect('/auth/cadastro')

        #Filtragem do banco de dados para saber se já existe o email cadastrado e enviar a respectiva mensagem
        usuario = User.objects.filter(email=email).first()
        if usuario: 
            messages.add_message(request, constants.WARNING, 'Este email já está em uso!')
            return redirect('/auth/cadastro')

        #Tratamento dos dados recebidos para não aceitar dados em branco
        if len(username.strip()) == 0 or len(email.strip()) == 0:    
            messages.add_message(request, constants.WARNING, 'O nome e o email não podem ser vazios!')
            return redirect('/auth/cadastro')


        #Utiliza da função criada em utils.py para validar senha
        if not password_is_valid(request, senha, confirmar_senha):
            return redirect('/auth/cadastro')

        #Tenta salvar no banco de dados 
        try:
            user = User.objects.create_user(username=username,
                                            email=email,
                                            password=senha,
                                            is_active=False)
            
            #Cria um token e salva no banco de dados para o usuario ativar pelo email
            token = sha256(f"{username}{email}".encode()).hexdigest()
            ativacao = Ativacao(token=token, user=user)
            ativacao.save()
            
            #Define o caminho da url do email
            path_template = os.path.join(settings.BASE_DIR, 'autenticacao/templates/email/conf_cadastro.html')
            #Chama a função para envio do email
            email_html(path_template, 'Cadastro confirmado', [email,], username=username, link_ativacao=f"127.0.0.1:8000/auth/ativar_conta/{token}")

            messages.add_message(request, constants.SUCCESS, 'Usuario cadastrado com sucesso')
            return redirect('/auth/login')
        
        except Exception as e:
            messages.add_message(request, constants.ERROR, f'Erro interno do sistema {e}')
            return redirect('/auth/cadastro')

#Função que é chamada ao acessar url /login
def logar(request):

    #Caso a requisição seja feita via url apenas renderizar as páginas 
    if request.method == "GET":

        #Se o usuário já está autenticado, renderizar pagina principal
        if request.user.is_authenticated:
            return redirect('/pacientes/')

        return render(request, 'login.html')
    
    #Caso a requisição seja POST, via formulário
    elif request.method == "POST":
        
        #Pega os dados do usuario
        username = request.POST.get('usuario')
        senha = request.POST.get('senha')

        usuario = User.objects.filter(username=username).first()
        #Filtra e retornar True caso o usuário não esteja ativo
        if not usuario.is_active:
            messages.add_message(request, constants.WARNING, 'Usuário precisa de ativação via email!')
            return redirect('/auth/login')
            
        #Confere se tem um usuário com esses dados no banco de dados
        usuario = auth.authenticate(username=username, password=senha)
        print(usuario)

        #Se não tiver, volta para o login e exibe o erro na tela
        if not usuario:
            messages.add_message(request, constants.ERROR, 'Username ou senha inválidos!')
            return redirect('/auth/login')
        
        #Senão, realiza o login e redireciona o usuário para a url principal
        else:
            auth.login(request, usuario)
            return redirect('/pacientes/')

#Função para realizar logout
def sair(request):
    auth.logout(request)
    return redirect('/auth/login')

#Função para ativar a conta
def ativar_conta(request, token):

    #Encontra o token no banco de dados ou retorna error 404
    token = get_object_or_404(Ativacao, token=token)
    
    if token.ativo:
        messages.add_message(request, constants.WARNING, 'Esse token já foi usado')
        return redirect('/auth/login')
    
    user = User.objects.get(username=token.user.username)
    user.is_active = True
    user.save()
    token.ativo = True
    token.save()
    messages.add_message(request, constants.SUCCESS, 'Conta ativada com sucesso')
    return redirect('/auth/login')
