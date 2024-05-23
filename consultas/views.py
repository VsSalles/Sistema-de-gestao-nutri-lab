from django.shortcuts import render, redirect, get_object_or_404
from plataforma.models import Pacientes, DadosPaciente
from django.http import HttpResponse, JsonResponse
from .models import Consulta, DadosConsulta, CodigoPedido, Cancelamento
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.contrib import messages
from .utils import valida_campo_branco, envia_email, gera_comprovante, gera_num_pedido
from hashlib import sha256
from secrets import token_hex
from datetime import timedelta, datetime

@login_required(login_url='/auth/login/')
def home(request):
    if request.method == 'GET':
        if request.GET.get('user'):
            user = request.GET.get('user')
            pacientes = Pacientes.objects.filter(id=user).filter()
            return render(request, 'consultas/consultas.html', {'pacientes': pacientes})
        pacientes = Pacientes.objects.filter(nutri=request.user)
        return render(request, 'consultas/consultas.html', {'pacientes': pacientes})
    elif request.method == 'POST':
        paciente_id = request.POST.get('paciente_id')
        data = request.POST.get('data_horario')
        local = request.POST.get('local')

        if not valida_campo_branco(paciente_id, data, local):
            messages.add_message(request, messages.WARNING, 'Todos os campos são obrigatórios!')
            return redirect('home')  

        paciente = get_object_or_404(Pacientes, pk=paciente_id)

        if not paciente.nutri == request.user:
            messages.add_message(request, messages.WARNING, 'Espertinho esse paciente não é seu!')
            return redirect('home')
        
        data = data.replace('T', ' ') + ':00' 
        data_formatada = datetime.strptime(data, '%Y-%m-%d %H:%M:%S')
        
        timestamp_data_recebida = data_formatada.timestamp()
        timestamp_data_atual = datetime.now().timestamp() 

        if timestamp_data_recebida < timestamp_data_atual:
            messages.add_message(request, messages.WARNING, 'Você não pode criar uma consulta no passado!')
            return redirect('home')

        try:
            codigo = gera_num_pedido(paciente)
            consulta = Consulta.objects.create(paciente=paciente, nutri=request.user, data_horario=data, local=local, status='A', codigo=codigo)
            consulta.save()
            messages.add_message(request, messages.SUCCESS, 'Consulta criada com sucesso!')
            return redirect('home')
        except Exception as e:
            messages.add_message(request, messages.ERROR, 'Erro interno do sistema!')
            print(e)
            return redirect('home')

@login_required(login_url='/auth/login/')
def agenda(request):
    nutri = request.user
    pacientes = Pacientes.objects.filter(nutri=nutri)
    consultas = Consulta.objects.filter(nutri=nutri)
    dados_consultas = DadosConsulta.objects.all()

    return render(request, 'consultas/agenda.html', {'consultas': consultas, 'dados_consultas': dados_consultas, 'pacientes': pacientes})

@login_required(login_url='/auth/login/')
def agenda_filter(request):
    data = request.GET.get('data')
    paciente = request.GET.get('paciente')
    status = request.GET.get('status')
    codigo = request.GET.get('codigo')
    db_pacientes = Pacientes.objects.filter(nutri=request.user)
    if len(data.strip()) != 0:
        try:
            data = datetime.strptime(data, '%Y-%m-%d')
            if paciente != 'T':
                if status == 'T':
                    consulta = Consulta.objects.filter(paciente=paciente).filter(data_horario = data).filter(nutri=request.user)
                    return render(request, 'consultas/agenda_filter.html', {'consultas': consulta, 'pacientes': db_pacientes})
                elif status != 'T':
                    consulta = Consulta.objects.filter(paciente=paciente).filter(status=status).filter(data_horario=data).filter(nutri=request.user)
                    return render(request, 'consultas/agenda_filter.html', {'consultas': consulta, 'pacientes': db_pacientes})
            
            elif status != 'T':
                consulta = Consulta.objects.filter(status=status).filter(data_horario=data).filter(nutri=request.user)
                return render(request, 'consultas/agenda_filter.html', {'consultas': consulta, 'pacientes': db_pacientes})

            elif len(codigo.strip()) > 0:
                consulta = Consulta.objects.filter(codigo=codigo).filter(data_horario=data).filter(nutri=request.user)
                return render(request, 'consultas/agenda_filter.html', {'consultas': consulta, 'pacientes': db_pacientes})
            else:
                consulta = Consulta.objects.filter(data_horario=data).filter(nutri=request.user)
                return render(request, 'consultas/agenda_filter.html', {'consultas': consulta, 'pacientes': db_pacientes})
            
        except Exception as e:
            messages.add_message(request, messages.ERROR, 'Data invalida')
            print(e)
            return redirect('agenda')
    else:
        if paciente != 'T':
            if status == 'T':
                consulta = Consulta.objects.filter(paciente=paciente).filter(nutri=request.user)
                return render(request, 'consultas/agenda_filter.html', {'consultas': consulta, 'pacientes': db_pacientes})
            elif status != 'T':
                consulta = Consulta.objects.filter(paciente=paciente).filter(nutri=request.user)
                return render(request, 'consultas/agenda_filter.html', {'consultas': consulta, 'pacientes': db_pacientes})
            
        elif status != 'T':
            consulta = Consulta.objects.filter(status=status).filter(nutri=request.user)
            return render(request, 'consultas/agenda_filter.html', {'consultas': consulta, 'pacientes': db_pacientes})

        elif len(codigo.strip()) > 0:
            pedido_db = get_object_or_404(CodigoPedido, pedido=codigo)
            consulta = Consulta.objects.filter(codigo=pedido_db).filter(nutri=request.user)
            return render(request, 'consultas/agenda_filter.html', {'consultas': consulta, 'pacientes': db_pacientes})
        else:
            return redirect('agenda')

@login_required(login_url='/auth/login/')
def realizar(request, pedido):
    pedido_db = get_object_or_404(CodigoPedido, pedido=pedido)
    consulta = Consulta.objects.filter(codigo=pedido_db).first()
    dados = DadosPaciente.objects.filter(paciente=consulta.paciente).last()
    paciente = get_object_or_404(Pacientes,id=consulta.paciente.id)
    if request.method == 'GET':   
        prazo_finalizar_consulta =  consulta.data_horario + timedelta(1)
        if consulta.data_horario > prazo_finalizar_consulta:
            messages.add_message(request, messages.WARNING, 'O prazo para finalizar essa consulta ja passou, vc deve cancelala, e justificar o motivo de não ter a finalizada em até 1 dias após a data da consulta')
            return redirect('agenda')      
        return render(request, 'consultas/realizar_consulta.html', {'consulta': consulta, 'dados': dados, 'paciente': paciente})
    elif request.method == 'POST':
        resumo = request.POST.get('resumo')
        objetivo = request.POST.get('objetivo')
        preferencia_alimentar = request.POST.get('preferencia_alimentar')
        horario_fome = request.POST.get('hora_fome')
        horas_sono = request.POST.get('horas_sono')
        tabagismo = request.POST.get('tabagismo')
        atividade = request.POST.get('atividade')

        if not valida_campo_branco(resumo, objetivo, preferencia_alimentar, horario_fome, horas_sono, tabagismo, atividade):
            messages.add_message(request, messages.WARNING, 'todos os campos ativos são obrigatorios!!')
            return redirect(f'/consultas/realizar/{pedido}/') 

        if not isinstance(horas_sono, str):
            messages.add_message(request, messages.WARNING, 'Digite numeros no campo horas_sono')
            return redirect(f'/consultas/realizar/{pedido}/') 

        if int(horas_sono) > 13:
            messages.add_message(request, messages.WARNING, 'Que sono é esse')
            return redirect(f'/consultas/realizar/{pedido}/')

        if tabagismo == 'N':
            frequencia_tabagismo = None
        else:
            frequencia_tabagismo = request.POST.get('frequencia_tab')

        if atividade == 'N':
            atividade_fisica = None
            horario_atividade = None
            qtd_dias_atividade = None
        else:
            atividade_fisica = request.POST.get('atividade_fisica')
            horario_atividade = request.POST.get('horario_atividade')
            qtd_dias_atividade = request.POST.get('dias_atv')

        try:
            dados_consulta = DadosConsulta.objects.create(consulta=consulta, resumo=resumo,objetivo=objetivo, preferencia_alimentar=preferencia_alimentar, 
                                                      horario_fome=horario_fome, horas_sono=horas_sono, tabagismo=tabagismo, 
                                                      frequencia_tabagismo=frequencia_tabagismo, atividade=atividade, atividade_fisica=atividade_fisica,
                                                      horario_atividade=horario_atividade, qtd_dias_atividade=qtd_dias_atividade,
                                                      )
            dados_consulta.save()
            consulta.status = 'F'
            consulta.save()
            messages.add_message(request, messages.SUCCESS, 'Consulta realizada com sucesso!')
            return redirect('agenda')
        except Exception as e:
            print(e)
            messages.add_message(request, messages.ERROR, 'erro interno do sistema')
            return redirect('agenda')

@login_required(login_url='/auth/login/')
def detalhes(request, pedido):
    pedido_db = get_object_or_404(CodigoPedido, pedido=pedido)
    consulta = Consulta.objects.filter(codigo=pedido_db).first()
    paciente = get_object_or_404(Pacientes, id=consulta.paciente.id)
    dados_consulta = DadosConsulta.objects.filter(consulta=consulta).first()
    dados_paciente = DadosPaciente.objects.filter(paciente=paciente).last()
    return render(request, 'consultas/detalhes.html',{'consulta':consulta, 'paciente': paciente, 'dados_paciente':dados_paciente, 'dados_consulta':dados_consulta})        

@login_required(login_url='/auth/login/')
def cancelar(request, pedido):
    pedido_db = get_object_or_404(CodigoPedido, pedido=pedido)
    consulta = get_object_or_404(Consulta, codigo=pedido_db)
    paciente = Pacientes.objects.get(id=consulta.paciente.id)


    if request.method == 'GET':
        return render(request, 'consultas/cancelar.html', {'consulta': consulta, 'paciente': paciente})

    if request.method == 'POST':
        motivo = request.POST.get('motivo')
        detalhes = request.POST.get('detalhes') 

        if consulta.status == 'F':
            messages.add_message(request, messages.INFO, 'Você não pode cancelar uma consulta finalizada!')
            return redirect('agenda')

        if Cancelamento.objects.filter(consulta=consulta).exists():
            messages.add_message(request, messages.INFO, 'Essa consulta ja foi cancelada!')
            return redirect('agenda')


        try:
            cancelamento = Cancelamento.objects.create(consulta=consulta, motivo=motivo, detalhes=detalhes)
            cancelamento.save()
            consulta.status = 'C'
            consulta.save()
            messages.add_message(request, messages.SUCCESS, 'Consulta cancelada com sucesso, enviamos um e-mail informando ao paciente')
            envia_email('consultas/email/cancelamento.html', 'consulta_cancelada', [consulta.paciente.email,], paciente=consulta.paciente, consulta=consulta, cancelamento=cancelamento)
            return redirect('agenda')
        except Exception as e:
            print(e)
            messages.add_message(request, messages.ERROR, 'Erro interno do servidor')
            return redirect('agenda')

@login_required(login_url='/auth/login/')
def motivo_cancelamento(request, pedido):
    pedido_db = get_object_or_404(CodigoPedido, pedido=pedido)
    consulta = get_object_or_404(Consulta, codigo=pedido_db)
    paciente = Pacientes.objects.get(id=consulta.paciente.id)
    cancelamento = get_object_or_404(Cancelamento, consulta=consulta)
    return render(request, 'consultas/motivo.html', {'paciente': paciente, 'consulta': consulta, 'cancelamento': cancelamento})

@login_required(login_url='/auth/login/')
def comprovante(request, pedido):
    pedido_db = get_object_or_404(CodigoPedido, pedido=pedido)
    consulta = get_object_or_404(Consulta, codigo=pedido_db)

    data_consulta = {
        'ano': datetime.strftime(consulta.data_horario, "%Y"),
        'mes': datetime.strftime(consulta.data_horario, "%m"),
        'dia': datetime.strftime(consulta.data_horario, "%d")
    }

    emissao = datetime.now()
    data_emissao = {
        'ano': datetime.strftime(emissao, '%Y'),
        'mes': datetime.strftime(emissao, '%m'),
        'dia': datetime.strftime(emissao, '%d')
    }

    if consulta.data_horario.hour < 12:
        periodo = 'manha'
    elif consulta.data_horario.hour > 11:
        periodo = 'tarde'
    elif consulta.data_horario.hour > 17:
        periodo = 'noite'
    chave = token_hex(32)
    token = sha256((consulta.paciente.email + consulta.paciente.nome + chave).encode()).hexdigest()
    try:
        gera_comprovante(
        consulta.paciente.nome, consulta.paciente.sobrenome, consulta.paciente.cpf, 
        data_consulta, periodo, consulta.local, token, consulta.nutri.username, data_emissao)
        messages.add_message(request, messages.SUCCESS, 'Comprovante gerado com sucesso!')
        return redirect(f'/consultas/detalhes/{pedido_db}/')
    except Exception as e:
            print(e)
            messages.add_message(request, messages.ERROR, 'Erro interno, tente mais tarde')
            return redirect(f'/consultas/detalhes/{pedido_db}/')   
  
@login_required(login_url='/auth/login/')
def gera_pdf(request, pedido):
   ...

