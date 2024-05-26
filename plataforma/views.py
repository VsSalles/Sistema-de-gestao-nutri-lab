from django.shortcuts import render, redirect, get_object_or_404 , HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . models import Pacientes, DadosPaciente, Refeicao, Opcao, GeraDados
from consultas.models import Consulta
from datetime import datetime
from . utils import valida_campos, gera_cpf, basal, Geradora, valida_campos_nulos
from django.views.decorators.csrf import csrf_exempt

@login_required(login_url='/auth/login/')
def pacientes(request):
    if request.method == 'GET': 
        print(request.user.username)
        paciente = Pacientes.objects.filter(nutri=request.user)
        return render(request, 'pacientes.html', {'pacientes': paciente})
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        sexo = request.POST.get('sexo')
        idade = request.POST.get('idade')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        
        if len(nome.strip()) == 0 or len(email.strip()) == 0 or len(telefone.strip()) == 0 or len(sexo.strip()) == 0 or len(idade.strip()) == 0 or len(sobrenome.strip()) == 0:
            messages.add_message(request, messages.ERROR, 'Todos os campos são obrigatorios!')
            return redirect('/pacientes/')
        
        if not idade.isnumeric():
            messages.add_message(request, messages.ERROR, 'Digite uma idade valida!')
            return redirect('/pacientes/')
        
        paciente = Pacientes.objects.filter(email=email)

        if paciente.exists():
            messages.add_message(request, messages.WARNING, 'Ja existe um paciente cadastrado com esse e-mail!')
            return redirect('/pacientes/')
        
        if int(idade) > 110:
            messages.add_message(request, messages.WARNING, 'Mais de 100 anos?')
            return redirect('/pacientes/')
        
        cpf = gera_cpf()
      
        try:
            p1 = Pacientes(nome=nome, sobrenome=sobrenome, cpf=cpf, sexo=sexo, idade=idade, email=email, telefone=telefone, nutri=request.user)
            p1.save()
            messages.add_message(request, messages.SUCCESS, 'Paciente cadastrado com sucesso!')
            return redirect('/pacientes/')
        except Exception as e:
            print(e)
            messages.add_message(request, messages.ERROR, 'Erro interno do sistema!')
            return redirect('/pacientes/')

@login_required(login_url='/auth/login')
def pacientes_filter(request):
    if request.method == 'GET':
        nome = request.GET.get('nome')
        email = request.GET.get('email')
        idade = request.GET.get('idade')
        paciente_id = request.GET.get('paciente')

        
        if paciente_id != 'todos':
            pacientes = Pacientes.objects.filter(id=paciente_id).filter(nutri = request.user)
        elif paciente_id == 'todos' and not nome and not email and not idade:
            pacientes = Pacientes.objects.filter(nutri=request.user)

        elif nome and email and idade:
            pacientes = Pacientes.objects.filter(nome__istartswith=nome).filter(email__icontains=email).filter(idade=idade).filter(nutri=request.user)

        elif nome and email:
            pacientes = Pacientes.objects.filter(nome__istartswith=nome).filter(email__icontains=email).filter(nutri=request.user)

        elif nome and idade:
            pacientes = Pacientes.objects.filter(nome__istartswith=nome).filter(idade=idade).filter(nutri=request.user)
        
        elif idade and email:
            pacientes = Pacientes.objects.filter(idade=idade).filter(email__icontains=email).filter(nutri=request.user)
        
        elif nome and idade:
            pacientes = Pacientes.objects.filter(nome__istartswith=nome).filter(idade=idade).filter(nutri=request.user)
        
        elif nome:
            pacientes = Pacientes.objects.filter(nome__istartswith=nome).filter(nutri=request.user)
        
        elif email:
            pacientes = Pacientes.objects.filter(nome__icontains=email).filter(nutri=request.user)

        else:
            pacientes = Pacientes.objects.filter(idade=idade).filter(nutri=request.user) 
        

        return render(request,'pacientes_filter.html', {'pacientes': pacientes})       

@login_required(login_url='/auth/login/')        
def dados_paciente(request, id):
    paciente = get_object_or_404(Pacientes, id=id)
    if not paciente.nutri == request.user:
        messages.add_message(request, messages.ERROR, 'Esse paciente não é seu')
        return redirect(f'/dados_paciente/{paciente.id}')
        
    if request.method == "GET":
        if request.GET.get('registro'):
            registro = request.GET.get('registro')
            dado_paciente = DadosPaciente.objects.filter(id=registro).first()
            dado_paciente_json = {
                'peso': dado_paciente.peso,
                'altura': dado_paciente.altura,
                'gordura': dado_paciente.percentual_gordura,
                'musculo': dado_paciente.percentual_musculo,
                'hdl': dado_paciente.colesterol_hdl,
                'ldl':  dado_paciente.colesterol_ldl,
                'ctotal': dado_paciente.colesterol_total,
                'triglicerídios': dado_paciente.trigliceridios

            }
            return JsonResponse({'dado_paciente': dado_paciente_json})
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

        if not valida_campos_nulos(peso, hdl, ldl, colesterol_total, altura, gordura, musculo, triglicerídios):
            messages.add_message(request, messages.WARNING, 'Todos os dados são obrigatorios, caso não saiba depois podera editar!')
            return redirect(f'/dados_paciente/{paciente.id}')
        
        if not int(peso) and int(altura) and int(gordura) and int(musculo) and int(hdl) and int(ldl) and int(colesterol_total) and int(triglicerídios):
            messages.add_message(request, messages.WARNING, 'Todos os dados são numericos!')
            return redirect(f'/dados_paciente/{paciente.id}')
        if int(peso) > 500:
            messages.add_message(request, messages.WARNING, 'Peso não pode ser maior que 500kg!')
            return redirect(f'/dados_paciente/{paciente.id}')
        
        if int(altura) > 300:
            messages.add_message(request, messages.WARNING, 'Altura não pode ser maior que 300cm ou 3m!')
            return redirect(f'/dados_paciente/{paciente.id}')
        
        if int(gordura) > 100:
            messages.add_message(request, messages.WARNING, 'Gordura não pode ser maior que 100%!')
            return redirect(f'/dados_paciente/{paciente.id}')
        
        if int(musculo) > 100:
            messages.add_message(request, messages.WARNING, 'Musculo não pode ser maior que 100%!')
            return redirect(f'/dados_paciente/{paciente.id}')

        p1 = {
            'sexo': paciente.sexo,
            'peso': int(peso),
            'altura': int(altura),
            'idade': int(paciente.idade)
        }
        taxa = basal(p1)
        if not valida_campos(request, peso, altura, gordura, musculo, hdl, ldl, colesterol_total, triglicerídios):
            messages.add_message(request, messages.WARNING, 'Digite todos os campos!')
            return redirect(f'/dados_paciente/{paciente.id}')
        else:
            try:
                paciente_dados = DadosPaciente(paciente=paciente,
                                        data=datetime.now(),
                                        peso=peso,
                                        altura=altura,
                                        taxa_metabolismo_basal = taxa,
                                        percentual_gordura=gordura,
                                        percentual_musculo=musculo,
                                        colesterol_hdl=hdl,
                                        colesterol_ldl=ldl,
                                        colesterol_total=colesterol_total,
                                        trigliceridios=triglicerídios)

                paciente_dados.save()
                messages.add_message(request, messages.SUCCESS, 'Dados cadastrados com sucesso')
                print(paciente.id)
                return redirect(f'/dados_paciente/{paciente.id}')


            except Exception as e:
                print(e)
                messages.add_message(request, messages.ERROR, 'Erro interno do sistema!')
                return redirect(f'/dados_paciente/{paciente.id}')

@login_required(login_url='/auth/login/')        
def atualiza_dados_paciente(request, id):
    paciente = get_object_or_404(Pacientes, id=id)
    peso = request.POST.get('peso')
    altura = request.POST.get('altura')
    gordura = request.POST.get('gordura')
    musculo = request.POST.get('musculo')
    hdl = request.POST.get('hdl')
    ldl = request.POST.get('ldl')
    ctotal = request.POST.get('ctotal')
    registro = request.POST.get('registro')
    triglicerídios = request.POST .get('triglicerídios')

    if not valida_campos_nulos(peso, altura, gordura, hdl, musculo, ldl, ctotal, registro, triglicerídios):
        messages.add_message(request, messages.warning, 'Todos os campos são obrigatorios')
        return redirect(f'/dados_paciente/{paciente.id}')
    
    dados_paciente = get_object_or_404(DadosPaciente, pk=registro)

        
    if not int(peso) and int(altura) and int(gordura) and int(musculo) and int(hdl) and int(ldl) and int(ctotal) and int(triglicerídios):
        messages.add_message(request, messages.WARNING, 'Todos os dados são numericos!')
        return redirect(f'/dados_paciente/{paciente.id}')
    if int(peso) > 500:
        messages.add_message(request, messages.WARNING, 'Peso não pode ser maior que 500kg!')
        return redirect(f'/dados_paciente/{paciente.id}')
        
    if int(altura) > 300:
        messages.add_message(request, messages.WARNING, 'Altura não pode ser maior que 300cm ou 3m!')
        return redirect(f'/dados_paciente/{paciente.id}')
        
    if int(gordura) > 100:
        messages.add_message(request, messages.WARNING, 'Gordura não pode ser maior que 100%!')
        return redirect(f'/dados_paciente/{paciente.id}')
        
    if int(musculo) > 100:
        messages.add_message(request, messages.WARNING, 'Musculo não pode ser maior que 100%!')
        return redirect(f'/dados_paciente/{paciente.id}')

    p1 = {
        'sexo': paciente.sexo,
        'peso': int(peso),
        'altura': int(altura),
        'idade': int(paciente.idade)
        }
    taxa = basal(p1)
    
    try: 
        dados_paciente.peso = int(peso)
        dados_paciente.altura = int(altura)
        dados_paciente.percentual_musculo = int(musculo)
        dados_paciente.percentual_gordura = int(gordura)
        dados_paciente.colesterol_hdl = int(hdl)
        dados_paciente.colesterol_ldl = int(ldl) 
        dados_paciente.trigliceridios = int(triglicerídios)
        dados_paciente.save()     
        messages.add_message(request, messages.SUCCESS, 'Dados atualizados com sucesso!')
        return redirect(f'/dados_paciente/{paciente.id}')

    except Exception as e:
        messages.add_message(request, messages.ERROR, 'Erro interno do sistema!')
        return redirect(f'/dados_paciente/{paciente.id}')
        
@login_required(login_url='/auth/login/')        
def pacientes_editar(request, id):
    try:
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        sexo = request.POST.get('sexo')
        idade = request.POST.get('idade')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')

        if not len(nome.strip()) or len(sexo.strip()) or len(idade.strip()) or len(email.strip()) or len(telefone.strip()) or len(sobrenome.strip()) or len(email.strip()):
            paciente = get_object_or_404(Pacientes, id=id)
            paciente.nome = nome
            paciente.sobrenome = sobrenome
            paciente.sexo = sexo
            paciente.idade = idade
            paciente.email = email
            paciente.telefone = telefone
            paciente.save()
            messages.add_message(request, messages.SUCCESS, 'Dados alterados com sucesso')
            return redirect('/dados_paciente/')
        else:
            messages.add_message(request, messages.WARNING, 'Todos os campos sao obrigatorios')
            return redirect('/dados_paciente/')
        
    except Exception as e:
        print(e)
        messages.add_message(request, messages.ERROR, 'Erro interno')
        return redirect('/dados_paciente/')

@login_required(login_url='/auth/login/')        
def pacientes_excluir(request, id):
    paciente = get_object_or_404(Pacientes, id=id)
    print(paciente)
    try:
        paciente.delete()
        messages.add_message(request, messages.SUCCESS, f'{paciente} excluido com sucesso')
        return redirect('/dados_paciente/')
    except Exception as e:
        print(e)
        messages.add_message(request, messages.ERROR, 'Erro interno')
        return redirect('/dados_paciente/')

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

@login_required(login_url='/auth/login/')        
def plano_alimentar_listar(request):
    if request.method == "GET":
        pacientes = Pacientes.objects.filter(nutri=request.user)
        return render(request, 'plano_alimentar_listar.html', {'pacientes': pacientes})

@login_required(login_url='/auth/login/')        
def plano_alimentar_filter(request):
    if request.method == 'GET':
        nome = request.GET.get('nome')
        email = request.GET.get('email')
        idade = request.GET.get('idade')
        paciente_id = request.GET.get('paciente')

        
        if paciente_id != 'todos':
            pacientes = Pacientes.objects.filter(id=paciente_id).filter(nutri = request.user)
        elif paciente_id == 'todos' and not nome and not email and not idade:
            pacientes = Pacientes.objects.filter(nutri=request.user)

        elif nome and email and idade:
            pacientes = Pacientes.objects.filter(nome__istartswith=nome).filter(email__icontains=email).filter(idade=idade).filter(nutri=request.user)

        elif nome and email:
            pacientes = Pacientes.objects.filter(nome__istartswith=nome).filter(email__icontains=email).filter(nutri=request.user)

        elif nome and idade:
            pacientes = Pacientes.objects.filter(nome__istartswith=nome).filter(idade=idade).filter(nutri=request.user)
        
        elif idade and email:
            pacientes = Pacientes.objects.filter(idade=idade).filter(email__icontains=email).filter(nutri=request.user)
        
        elif nome and idade:
            pacientes = Pacientes.objects.filter(nome__istartswith=nome).filter(idade=idade).filter(nutri=request.user)
        
        elif nome:
            pacientes = Pacientes.objects.filter(nome__istartswith=nome).filter(nutri=request.user)
        
        elif email:
            pacientes = Pacientes.objects.filter(nome__icontains=email).filter(nutri=request.user)

        else:
            pacientes = Pacientes.objects.filter(idade=idade).filter(nutri=request.user) 
        

        return render(request,'plano_alimentar_filter.html', {'pacientes': pacientes}) 

@login_required(login_url='/auth/login/')        
def plano_alimentar(request, id):
    paciente = get_object_or_404(Pacientes, id=id)
    if not paciente.nutri == request.user:
        messages.add_message(request, messages.ERROR, 'Esse paciente não é seu')
        return redirect('/dados_paciente/')

    if request.method == "GET":
        if request.GET.get('identificador'):
            identificador = request.GET.get('identificador')
            refeicao = Refeicao.objects.filter(id=identificador).first()

            json = {
                'titulo': refeicao.titulo,
                'horario': refeicao.horario,
                'carboidratos': refeicao.carboidratos,
                'proteinas': refeicao.proteinas,
                'gorduras': refeicao.gorduras,

            }
            return JsonResponse({'dados_refeicao': json})
        
        elif request.GET.get('identificador_op'):
            identificador_op = request.GET.get('identificador_op')
            opcao = Opcao.objects.filter(id=identificador_op).first()

            json = {
                'descricao': opcao.descricao              
            }
            return JsonResponse({'dados_opcao': json})
        
        r1 = Refeicao.objects.filter(paciente=paciente).order_by('horario')
        opcaoes = Opcao.objects.all()
        opcao = []
        for op in opcaoes:
            if op.refeicao.paciente == paciente:
                opcao.append(op)
            
        return render(request, 'plano_alimentar.html', {'paciente': paciente, 'refeicao': r1, 'opcao': opcao})

@login_required(login_url='/auth/login/')        
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

@login_required(login_url='/auth/login/')        
def opcao(request, id_paciente):
    if request.method == "POST":
        id_refeicao = request.POST.get('refeicao')
        imagem = request.FILES.get('imagem')
        descricao = request.POST.get("descricao")

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

@login_required(login_url='/auth/login/')        
def edita_refeicao(request, id_paciente):
     paciente = get_object_or_404(Pacientes, id=id_paciente)
     if not paciente.nutri == request.user:
        messages.add_message(request, messages.ERROR, 'Esse paciente não é seu')
        return redirect('/dados_paciente/')

     if request.method == "POST":
        identificador = request.POST.get('identificador')
        titulo = request.POST.get('titulo')
        horario = request.POST.get('horario')
        carboidratos = request.POST.get('carboidratos')
        proteinas = request.POST.get('proteinas')
        gorduras = request.POST.get('gorduras')

        refeicao = get_object_or_404(Refeicao, id=identificador)

        try:
            refeicao.titulo = titulo
            refeicao.horario = horario
            refeicao.carboidratos = carboidratos
            refeicao.proteinas = proteinas
            refeicao.gorduras = gorduras
            refeicao.save()
            messages.add_message(request, messages.SUCCESS, 'Refeição atualizada com sucesso!')
            return redirect(f'/plano_alimentar/{id_paciente}')
        except Exception as e:
            print(e)
            messages.add_message(request, messages.ERROR, 'Erro interno do sistema')
            return redirect(f'/plano_alimentar/{id_paciente}')

@login_required(login_url='/auth/login/')        
def edita_opcao(request, id_paciente):
     paciente = get_object_or_404(Pacientes, id=id_paciente)
     if not paciente.nutri == request.user:
        messages.add_message(request, messages.ERROR, 'Esse paciente não é seu')
        return redirect('/dados_paciente/')

     if request.method == "POST":
        identificador = request.POST.get('opcao')
        imagem = request.POST.get('imagem')
        descricao = request.POST.get('descricao')

        opcao = get_object_or_404(Opcao, id=identificador)

        try:
            if imagem:
                opcao.imagem = imagem
            opcao.descricao = descricao
            opcao.save()
            messages.add_message(request, messages.SUCCESS, 'Opção atualizada com sucesso!')
            return redirect(f'/plano_alimentar/{id_paciente}')
        except Exception as e:
            print(e)
            messages.add_message(request, messages.ERROR, 'Erro interno do sistema')
            return redirect(f'/plano_alimentar/{id_paciente}')

@login_required(login_url='/auth/login/')   
def exclui_refeicao(request, id_paciente):
    paciente = get_object_or_404(Pacientes, id=id_paciente)
    if not paciente.nutri == request.user:
        messages.add_message(request, messages.ERROR, 'Esse paciente não é seu')
        return redirect('/dados_paciente/')

    if request.method == "POST":
        identificador = request.POST.get('identificador')

        refeicao = get_object_or_404(Refeicao, id=identificador)

        try:
            refeicao.delete()
            messages.add_message(request, messages.INFO, 'Refeição excluida com sucesso!')
            return redirect(f'/plano_alimentar/{id_paciente}')
        except Exception as e:
            print(e)
            messages.add_message(request, messages.ERROR, 'Erro interno do sistema')
            return redirect(f'/plano_alimentar/{id_paciente}')

@login_required(login_url='/auth/login/')   
def exclui_opcao(request, id_paciente):
    paciente = get_object_or_404(Pacientes, id=id_paciente)
    if not paciente.nutri == request.user:
        messages.add_message(request, messages.ERROR, 'Esse paciente não é seu')
        return redirect('/dados_paciente/')

    if request.method == "POST":
        identificador = request.POST.get('opcao')

        opcao = get_object_or_404(Opcao, id=identificador)

        try:
            opcao.delete()
            messages.add_message(request, messages.INFO, 'Opção excluida com sucesso!')
            return redirect(f'/plano_alimentar/{id_paciente}')
        except Exception as e:
            print(e)
            messages.add_message(request, messages.ERROR, 'Erro interno do sistema')
            return redirect(f'/plano_alimentar/{id_paciente}')

@login_required(login_url='/auth/login/')        
def dashboard(request):
    qtd_pacientes = len(Pacientes.objects.filter(nutri=request.user))
    qtd_consultas = len(Consulta.objects.filter(nutri=request.user))
    usuario = request.user
    return render(request, 'dashboard.html', {'qtd_pacientes': qtd_pacientes, 'qtd_consultas': qtd_consultas, 'user': usuario})

@login_required(login_url='/auth/login/')        
def gerar_dados(request): 
    limite = GeraDados.objects.filter(nutri=request.user).first()
    if limite:
        limites = {'limite': limite.limite}
        messages.add_message(request, messages.INFO, 'IMPORTANTE, essa funcionalidade foi desenvolivda apenas para testar o sistema e esta em fase BETA pode correr bugs, os dados gerados são ficticios e serão apagados assim que o logout for realizado')
        return render(request, 'gerar.html', limites)
    else:
        limite = GeraDados.objects.create(nutri=request.user, limite=0)
        limites = {'limite': limite.limite}
        messages.add_message(request, messages.INFO, 'MPORTANTE, essa funcionalidade foi desenvolivda apenas para testar o sistema e esta em fase BETA pode correr bugs, os dados gerados são ficticios e serão apagados assim que o logout for realizado')
        return render(request, 'gerar.html', limites)

@login_required(login_url='/auth/login/')        
def gerar_tudo(request):
    qtd_dados = request.GET.get('qtd_dados')
    limite = GeraDados.objects.filter(nutri=request.user).first()
    try: 
        qtd_dados = int(qtd_dados) 
    except ValueError: 
        messages.add_message(request, messages.WARNING, 'Por favor envie apenas um numero inteiro até 40')
        return redirect('gerar')
    
    if limite.limite + qtd_dados > 40:
        messages.add_message(request, messages.WARNING , 'Você ultrapassara seu limte de 40 dados!!')
        return redirect('gerar')

    if qtd_dados > 40:
        messages.add_message(request, messages.WARNING, 'Você só pode gerar até 40 dados!!')
        return redirect('gerar')
    
    gerar = Geradora(request.user, qtd_dados=qtd_dados,  limite=limite.limite)

    try: 
        print(gerar.gera_consulta())
        limite.limite = limite.limite + qtd_dados
        limite.save()
        messages.add_message(request, messages.SUCCESS, 'Dados gerados com sucesso')
        return redirect('gerar')
    except Exception as e:
        print(e)
        messages.add_message(request, messages.ERROR, 'Erro interno do sistema, tente mais tarde')
        return redirect('gerar')


    

    


