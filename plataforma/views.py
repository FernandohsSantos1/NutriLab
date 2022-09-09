from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import constants
from .models import Pacientes, DadosPaciente, Refeicao, Opcao
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

#Decorador para caso o login_required, caso o usuário não esteja logado
#envia para a url de login, se não chama a função pacientes
@login_required(login_url='/auth/login/')
def pacientes(request):
    
    #If para diferenciar requisições GET e POST
    if request.method == "GET":
        #Cria variavel pacientes que recebe todos os pacientes que são 
        #do nutricionista logado e envia para o front-end
        pacientes = Pacientes.objects.filter(nutri=request.user)
        return render(request, 'pacientes.html', {'pacientes': pacientes})
    
    elif request.method == "POST":
        #Pega as variáves do formulário
        nome = request.POST.get('nome')
        sexo = request.POST.get('sexo')
        idade = request.POST.get('idade')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        
        #Verificação de dados em branco
        if (len(nome.strip()) == 0) or (len(sexo.strip()) == 0) or (len(idade.strip()) == 0) or (len(email.strip()) == 0) or (len(telefone.strip()) == 0):
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
            return redirect('/pacientes/')
        
        #Verificação se idade é numérico
        if not idade.isnumeric():
            messages.add_message(request, constants.ERROR, 'Digite uma idade válida')
            return redirect('/pacientes/')

        #Verificação se o email já está em uso   
        pacientes = Pacientes.objects.filter(email=email)
        if pacientes.exists():
            messages.add_message(request, constants.ERROR, 'Já existe um paciente com esse E-mail')
            return redirect('/pacientes/')

        #Tenta salvar os dados no banco de dados
        try:
            paciente = Pacientes(   nome=nome,
                                    sexo=sexo,
                                    idade=idade,
                                    email=email,
                                    telefone=telefone,
                                    nutri=request.user)
            paciente.save()
            messages.add_message(request, constants.SUCCESS, 'Paciente cadastrado com sucesso')
            return redirect('/pacientes/')
        
        except:
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
            return redirect('/pacientes/')
        
    return HttpResponse(f"{nome}, {sexo}, {idade}, {email}, {telefone}")

#Função para listar os pacientes
@login_required(login_url='/auth/login/')
def dados_paciente_listar(request):
    if request.method == "GET":
        pacientes = Pacientes.objects.filter(nutri=request.user)
        return render(request, 'dados_paciente_listar.html', {'pacientes': pacientes})

#Função que exibe dados de cada paciente, um por vez
@login_required(login_url='/auth/login/')
def dados_paciente(request, id):
    paciente = get_object_or_404(Pacientes, id=id)
    #Caso o nutricionista tente acessar uma url pelo id de outro paciente
    #é retornado uma mensagem de erro
    if not paciente.nutri == request.user:
        messages.add_message(request, constants.ERROR, 'Esse paciente não é seu')
        return redirect('/dados_paciente/')
    
    if request.method == "GET":
        dados_paciente = DadosPaciente.objects.filter(paciente=paciente)
        return render(request, 'dados_paciente.html', {'paciente': paciente, 'dados_paciente': dados_paciente})
        
    elif request.method == "POST":
        #Pega os dados do formulário
        peso = request.POST.get('peso')
        altura = request.POST.get('altura')
        gordura = request.POST.get('gordura')
        musculo = request.POST.get('musculo')
        hdl = request.POST.get('hdl')
        ldl = request.POST.get('ldl')
        colesterol_total = request.POST.get('ctotal')
        triglicerídios = request.POST.get('triglicerídios')
        
        #Salva os dados do paciente no banco de dados
        paciente = DadosPaciente(paciente=paciente,
                                data=datetime.now(),
                                peso=peso,
                                altura=altura,
                                percentual_gordura=gordura,
                                percentual_musculo=musculo,
                                colesterol_hdl=hdl,
                                colesterol_ldl=ldl,
                                colesterol_total=colesterol_total,
                                trigliceridios=triglicerídios)
        
        paciente.save()

        messages.add_message(request, constants.SUCCESS, 'Dados cadastrado com sucesso')
    
        
        return redirect('/dados_paciente/')

#Função para exibir o gráfico de evolução do paciente ao longo do tempo
@login_required(login_url='/auth/login/')
@csrf_exempt
def grafico_peso(request, id):
    paciente = Pacientes.objects.get(id=id)
    dados = DadosPaciente.objects.filter(paciente=paciente).order_by("data")
    
    pesos = [dado.peso for dado in dados]
    labels = list(range(len(pesos)))
    data = {'peso': pesos,
            'labels': labels}
    return JsonResponse(data)

#Função para listar o plano alimentar dos pacientes
@login_required(login_url='/auth/login/')
def plano_alimentar_listar(request):
    if request.method == "GET":
        pacientes = Pacientes.objects.filter(nutri=request.user)
        return render(request, 'plano_alimentar_listar.html', {'pacientes': pacientes})

#Função para listar o plano alimentar por paciente
@login_required(login_url='/auth/login/')
def plano_alimentar(request, id):
    paciente = get_object_or_404(Pacientes, id=id)
    if not paciente.nutri == request.user:
        messages.add_message(request, constants.ERROR, 'Esse paciente não é seu')
        return redirect('/plano_alimentar_listar/')

    if request.method == "GET":
        r1 = Refeicao.objects.filter(paciente=paciente).order_by('horario')
        opcao = Opcao.objects.all()
        return render(request, 'plano_alimentar.html', {'paciente': paciente, 'refeicao': r1, 'opcao': opcao})

#Função para cadastro das refeições com os macro nutrientes indicados
@login_required(login_url='/auth/login/')
def refeicao(request, id_paciente):
    paciente = get_object_or_404(Pacientes, id=id_paciente)
    if not paciente.nutri == request.user:
        messages.add_message(request, constants.ERROR, 'Esse paciente não é seu')
        return redirect('/dados_paciente/')

    if request.method == "POST":
        titulo = request.POST.get('titulo')
        horario = request.POST.get('horario')
        carboidratos = request.POST.get('carboidratos')
        proteinas = request.POST.get('proteinas')
        gorduras = request.POST.get('gorduras')

        r1 = Refeicao(paciente=paciente,
                      titulo=titulo,
                      horario=horario,
                      carboidratos=carboidratos,
                      proteinas=proteinas,
                      gorduras=gorduras)

        r1.save()

        messages.add_message(request, constants.SUCCESS, 'Refeição cadastrada')
        return redirect(f'/plano_alimentar/{id_paciente}')

#Função para cadastro de opções para cada refeição, o nutricionista
#pode enviar fotos
@login_required(login_url='/auth/login/')
def opcao(request, id_paciente):
    if request.method == "POST":
        id_refeicao = request.POST.get('refeicao')
        imagem = request.FILES.get('imagem')
        descricao = request.POST.get("descricao")

        o1 = Opcao(refeicao_id=id_refeicao,
                   imagem=imagem,
                   descricao=descricao)

        o1.save()

        messages.add_message(request, constants.SUCCESS, 'Opção cadastrada')
        return redirect(f'/plano_alimentar/{id_paciente}')

#Função para excluir o paciente
@login_required(login_url='/auth/login/')
def excluir(request, id_paciente):
    paciente = get_object_or_404(Pacientes, id=id_paciente)
    
    if not paciente.nutri == request.user:
        messages.add_message(request, constants.ERROR, 'Somente a nutricionista pode remover seus pacientes!')
        return redirect('/pacientes/')
    
    try:
        paciente.delete()
        messages.add_message(request, constants.SUCCESS, 'Paciente removido com sucesso')
        return redirect('/pacientes/')
    
    except:
        messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
        return redirect('/pacientes/')

#Função para atualizar os dados cadastrais do paciente
@login_required(login_url='/auth/login/')
def atualizar(request, id_paciente):
    paciente = get_object_or_404(Pacientes, id=id_paciente)
    
    if not paciente.nutri == request.user:
        messages.add_message(request, constants.ERROR, 'Somente a nutricionista pode remover seus pacientes!')
        return redirect('/pacientes/')
    
    try:
        nome = request.POST.get('nome')
        sexo = request.POST.get('sexo')
        idade = request.POST.get('idade')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')

        paciente.nome = nome
        paciente.sexo = sexo
        paciente.idade = idade
        paciente.email = email
        paciente.telefone = telefone
        
        paciente.save()
        messages.add_message(request, constants.SUCCESS, 'Paciente alterado com sucesso')
        return redirect('/pacientes/')


    except:
        messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
        return redirect('/pacientes/')