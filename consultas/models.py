from django.db import models
from plataforma.models import Pacientes
from django.contrib.auth.models import User
import datetime


class CodigoPedido(models.Model):
    pedido = models.CharField(max_length=20000, unique=True)
    paciente = models.ForeignKey(Pacientes, on_delete=models.CASCADE)
    data = models.DateTimeField(default=datetime.datetime.now())

    def __str__(self) -> str:
        return self.pedido

class Consulta(models.Model):
    choice_status = (('A', 'agendada'),('C', 'cancelada'), ('F', 'finalizada')) 
    paciente = models.ForeignKey(Pacientes, on_delete=models.CASCADE)
    nutri = models.ForeignKey(User, on_delete=models.CASCADE)
    data_horario = models.DateTimeField()
    local = models.TextField(blank=True, default='São Paulo, Toninho Cerezo 820, andar 8')
    status = models.CharField(max_length=1, choices=choice_status)
    codigo = models.OneToOneField(CodigoPedido, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.paciente.nome}|{self.codigo}'
    
class DadosConsulta(models.Model):
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE, blank=True, null=True)
    choice = (('S', 'sim'),('N','não') )
    choice_fisica = (('A', 'academia'), ('N', 'natacao'), ('C', 'corrida'), ('L', 'luta'), ('O', 'outro'))
    choice_objetivo = (('M', 'massa muscular'), ('D', 'definição'), ('S', 'vida_saudavel'))
    choice_tabagismo = (('1M', '1 maço por dia'), ('2M', '2 maços por dia'), ('M+', 'mais de 2 maços por dia'), ('M-', 'menos de 1 maço por dia'))
    resumo = models.TextField()
    objetivo = models.CharField(max_length=1, choices=choice_objetivo)
    preferencia_alimentar = models.TextField()
    horario_fome = models.TimeField()
    horas_sono = models.IntegerField()
    tabagismo = models.CharField(max_length=1, choices=choice)
    frequencia_tabagismo = models.CharField(max_length=2, choices=choice_tabagismo, blank=True, null=True)
    atividade_fisica = models.CharField(max_length=1, choices=choice)
    atividade = models.CharField(max_length=1, choices=choice_fisica, blank=True, null=True)
    horario_atividade = models.TimeField(blank=True, null=True)
    qtd_dias_atividade = models.IntegerField(default=3, blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.consulta.paciente.nome}|{self.consulta.codigo}'
    
class Cancelamento(models.Model):
    choice_motivo = (('E', 'Emergencia'), ('I', 'imprevisto'), ('O', 'Outro'))
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE, blank=True, null=True)
    motivo = models.CharField(max_length=1, choices=choice_motivo)
    detalhes = models.TextField(blank=True, null=True)
    data = models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        if self.motivo == 'E':
            return f'{self.consulta.codigo}|Emergencial'
        elif self.motivo == 'I':
            return f'{self.consulta.codigo}|Imprevisto'
        else:
            return f'{self.consulta.codigo}|Outro'