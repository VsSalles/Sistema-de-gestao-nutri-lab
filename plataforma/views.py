from django.shortcuts import render, redirect, get_object_or_404 
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . models import Pacientes, DadosPaciente, Refeicao, Opcao
from datetime import datetime
from . utils import valida_campos

@login_required(login_url='/auth/login/')
def pacientes(request):
    if request.method == 'GET': 
        paciente = Pacientes.objects.filter(nutri=request.user)
        return render(request, 'pacientes.html', {'pacientes': paciente})
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        sexo = request.POST.get('sexo')
        idade = request.POST.get('idade')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        
        if len(nome.strip()) == 0 or len(email.strip()) == 0 or len(telefone.strip()) == 0 or len(sexo.strip()) == 0 or len(idade.strip()) == 0:
            messages.add_message(request, messages.ERROR, 'Todos os campos são obrigatorios!')
            return redirect('/pacientes/')
        
        if not idade.isnumeric():
            messages.add_message(request, messages.ERROR, 'Digite uma idade valida!')
            return redirect('/pacientes/')
        
        paciente = Pacientes.objects.filter(email=email)

        if paciente.exists():
            messages.add_message(request, messages.WARNING, 'Ja existe um paciente cadastrado com esse e-mail!')
            return redirect('/paciente/')
        
        try:
            p1 = Pacientes(nome=nome, sexo=sexo, idade=idade, email=email, telefone=telefone, nutri=request.user)
            p1.save()
            messages.add_message(request, messages.SUCCESS, 'Paciente cadastrado com sucesso!')
            return redirect('/pacientes/')
        except Exception as e:
            print(e)
            messages.add_message(request, messages.ERROR, 'Erro interno do sistema!')
            return redirect('/pacientes/')
        
@login_required(login_url='/auth/login/')        
def dados_paciente_listar(request):
    if request.method == 'GET':
        pacientes = Pacientes.objects.filter(nutri=request.user)
        return render(request, 'dados_paciente_listar.html', {'pacientes': pacientes})        

def dados_paciente(request, id):

    paciente = get_object_or_404(Pacientes, id=id)
    if not paciente.nutri == request.user:
        messages.add_message(request, messages.ERROR, 'Esse paciente não é seu')
        return redirect('/dados_paciente/')
        
    if request.method == "GET":
        dados_paciente = DadosPaciente.objects.filter(paciente=paciente)
        return render(request, 'dados_paciente.html', {'paciente': paciente, 'dados_paciente': dados_paciente})
    
    elif request.method == "POST":
        peso = request.POST.get('peso')
        altura = request.POST.get('altura')
        gordura = request.POST.get('gordura')
        musculo = request.POST.get('musculo')
        hdl = request.POST.get('hdl')
        ldl = request.POST.get('ldl')
        colesterol_total = request.POST.get('ctotal')
        triglicerídios = request.POST.get('triglicerídios')

        if not valida_campos(request, peso, altura, gordura, musculo, hdl, ldl, colesterol_total, triglicerídios):
            return redirect('/dados_paciente/')
        else:
            try:
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
                messages.add_message(request, messages.SUCCESS, 'Dados cadastrados com sucesso')
            except Exception as e:
                print(e)
                messages.add_message(request, messages.ERROR, 'Erro interno do sistema!')
                return redirect('/dados_paciente/')

        messages.add_message(request, messages.SUCCESS, 'Dados cadastrado com sucesso')

        return redirect('/dados_paciente/')
    
from django.views.decorators.csrf import csrf_exempt

@login_required(login_url='/auth/logar/')
@csrf_exempt
def grafico_peso(request, id):

    paciente = Pacientes.objects.get(id=id)
    dados = DadosPaciente.objects.filter(paciente=paciente).order_by("data")
    
    pesos = [dado.peso for dado in dados]
    labels = list(range(len(pesos)))
    data = {'peso': pesos,
            'labels': labels}
    return JsonResponse(data)

def plano_alimentar_listar(request):
    if request.method == "GET":
        pacientes = Pacientes.objects.filter(nutri=request.user)
        return render(request, 'plano_alimentar_listar.html', {'pacientes': pacientes})
    
def plano_alimentar(request, id):
    paciente = get_object_or_404(Pacientes, id=id)
    if not paciente.nutri == request.user:
        messages.add_message(request, messages.ERROR, 'Esse paciente não é seu')
        return redirect('/dados_paciente/')

    if request.method == "GET":
        r1 = Refeicao.objects.filter(paciente=paciente).order_by('horario')
        opcao = Opcao.objects.all()
        return render(request, 'plano_alimentar.html', {'paciente': paciente, 'refeicao': r1, 'opcao': opcao})
    
def refeicao(request, id_paciente):
    paciente = get_object_or_404(Pacientes, id=id_paciente)
    if not paciente.nutri == request.user:
        messages.add_message(request, messages.ERROR, 'Esse paciente não é seu')
        return redirect('/dados_paciente/')

    if request.method == "POST":
        titulo = request.POST.get('titulo')
        horario = request.POST.get('horario')
        carboidratos = request.POST.get('carboidratos')
        proteinas = request.POST.get('proteinas')
        gorduras = request.POST.get('gorduras')

        if len(titulo.strip()) == 0 or len(horario.strip()) == 0  or len(carboidratos.strip()) == 0 or len(proteinas.strip()) == 0 or len(gorduras.strip()) == 0:
            messages.add_message(request, messages.WARNING, 'todos os campos são obrigatorios!')
            return redirect('plano_alimentar',paciente.id)

        try:
            r1 = Refeicao(paciente=paciente,
                        titulo=titulo,
                        horario=horario,
                        carboidratos=carboidratos,
                        proteinas=proteinas,
                        gorduras=gorduras)

            r1.save()
            messages.add_message(request, messages.SUCCESS, 'Refeição cadastrada com sucesso!')
            return redirect(f'/plano_alimentar/{id_paciente}')
        except Exception as e:
            print(e)
            messages.add_message(request, messages.ERROR, 'Erro interno do sistema')
            return redirect(f'/plano_alimentar/{id_paciente}')

def opcao(request, id_paciente):
    if request.method == "POST":
        id_refeicao = request.POST.get('refeicao')
        imagem = request.FILES.get('imagem')
        descricao = request.POST.get("descricao")
        print(type(id_refeicao))
        print(type(imagem))
        print(type(descricao))

        if id_refeicao == None or len(descricao.strip()) == 0 or imagem == None:
            messages.add_message(request, messages.WARNING, 'Refeição, descrição e imagem obrigatorios')
            return redirect('plano_alimentar', id_paciente)


        try:
            o1 = Opcao(refeicao_id=id_refeicao,
                    imagem=imagem,
                    descricao=descricao)
            o1.save()
            messages.add_message(request, messages.SUCCESS, 'Opcao cadastrada')
            return redirect(f'/plano_alimentar/{id_paciente}')
        except Exception as e:
            print(e)
            return redirect('plano_alimentar', id_paciente)

    


