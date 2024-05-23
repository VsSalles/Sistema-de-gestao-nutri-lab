from ninja import Router
from datetime import datetime
from consultas.models import Consulta, Pacientes, DadosConsulta, Cancelamento
from django.shortcuts import get_object_or_404

plataforma_router = Router()

@plataforma_router.get('/relatorio_consultas/{user}')
def relatorio_consultas(request, user):
    consultas = Consulta.objects.filter(nutri=user)
    data = []
    labels = []
    mes = datetime.now().month + 1
    ano = datetime.now().year
    meses = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
    for x in range(12):
        mes -= 1
        if mes == 0:
            mes = 12
            ano -= 1
        
        y = len([x.data_horario for x in consultas if x.data_horario.month == mes and x.data_horario.year == ano])
        labels.append(meses[mes-1])
        data.append(y)
    
    data_json = {'data': data, 'labels': labels}

    return data_json

@plataforma_router.get('/relatorio_consultas_status/{user}')
def relatorio_consultas(request, user):
    consultas = Consulta.objects.filter(nutri=user)
    qtd_consultas = len(consultas)
    consultas_c= len(consultas.filter(status='C'))    
    consultas_f = len(consultas.filter(status='F'))     
    consultas_a = len(consultas.filter(status='A')) 
    labels = ['Total de consultas', 'Consultas Finalizadas', 'Consultas Agendadas', 'Consultas Canceladas']
    data = [qtd_consultas, consultas_f, consultas_a, consultas_c]
    data_json = {'data': data, 'labels': labels}

    return data_json

@plataforma_router.get('/relatorio_consultas_canceladas/{user}')
def relatorio_consultas(request, user):
    consultas_user = Consulta.objects.filter(nutri=user)
    consultas_canc = Cancelamento.objects.filter(consulta__in=consultas_user)
    consultas_t = len(consultas_canc)
    consultas_e = len([x for x in consultas_canc if x.motivo == 'E'])
    consultas_i = len([x for x in consultas_canc if x.motivo == 'I'])
    consultas_o = len([x for x in consultas_canc if x.motivo == 'O'])
    labels = ['Total Consultas Canceladas', 'Emergencial', 'Imprevisto', 'Outro']
    data = [consultas_t, consultas_e, consultas_i, consultas_o]
    data_json = {'data': data, 'labels': labels}

    return data_json

@plataforma_router.get('/relatorio_pacientes/{user}')
def relatorio_pacientes(request, user):
    pacientes = Pacientes.objects.filter(nutri=user)
    consultas = Consulta.objects.filter(nutri=user)
    qtd_pacientes = len(pacientes)
    pacientes_m = len(pacientes.filter(sexo='M'))    
    pacientes_f = len(pacientes.filter(sexo='F'))   
    pacientes_c = [x.paciente.nome for x in consultas] 
    pacientes_c = list(set(pacientes_c)) 
    media_idade = 0
    if not len(pacientes) == 0:
        media_idade = sum([x.idade for x in pacientes]) / len(pacientes)
    
    data = [qtd_pacientes ,pacientes_m, pacientes_f, f'{media_idade:.0f}', len(pacientes_c)]
    labels = ['Total de Pacientes','Masculino', 'Feminino', 'Média de Idade', 'QTD, Pacientes que ja realizaram/agendaram consulta']          
    data_json = {'data': data, 'labels': labels}
    return data_json

@plataforma_router.get('/relatorio_pacientes_objetivos/{user}')
def relatorio_pacientes(request, user):
    consultas_user = Consulta.objects.filter(nutri=user)
    consultas = DadosConsulta.objects.filter(consulta__in = consultas_user)
    

    pacientes_m = len([x.objetivo for x in consultas if x.objetivo == 'M'])
    pacientes_d = len([x.objetivo for x in consultas if x.objetivo == 'D'])
    pacientes_v = len([x.objetivo for x in consultas if x.objetivo == 'S'])

    data = [pacientes_m ,pacientes_d, pacientes_v]
    labels = ['Massa Muscular','Definição Muscular', 'Vida Saudavel']          
    data_json = {'data': data, 'labels': labels}
    return data_json

@plataforma_router.get('/relatorio_pacientes_atv/{user}')
def relatorio_pacientes(request, user):
    consultas_user = Consulta.objects.filter(nutri=user)
    consultas = DadosConsulta.objects.filter(consulta__in = consultas_user)

    pacientes_a = len([x.atividade for x in consultas if x.atividade == 'A'])
    pacientes_l = len([x.atividade for x in consultas if x.atividade == 'L'])
    pacientes_c = len([x.atividade for x in consultas if x.atividade == 'C'])
    pacientes_n = len([x.atividade for x in consultas if x.atividade == 'N'])
    pacientes_o = len([x.atividade for x in consultas if x.atividade == 'O'])


    data = [pacientes_a ,pacientes_l, pacientes_c, pacientes_n, pacientes_o]
    labels = ['Academia','Luta', 'Corrida', 'Natação', 'Outro']          
    data_json = {'data': data, 'labels': labels}
    return data_json

