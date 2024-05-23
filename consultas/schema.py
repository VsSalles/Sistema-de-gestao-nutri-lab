from ninja import ModelSchema, Schema
from . models import Consulta as ModelConsultas
from . models import DadosConsulta as ModelDadosConsulta
from plataforma.models import Pacientes
from django.contrib.auth.models import User
from typing import List 
from datetime import datetime

class Consultas(ModelSchema):
    paciente: int
    data_horario : str
    class Config:
        model = ModelConsultas
        model_fields = '__all__'
        model_exclue = ['status']
        

class DadosConsultas(ModelSchema):
    class Config:
        model = ModelDadosConsulta
        model_fields = '__all__'



    