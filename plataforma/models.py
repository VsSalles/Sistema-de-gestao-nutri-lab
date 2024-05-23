from django.db import models
from django.contrib.auth.models import User

class Pacientes(models.Model):
    choices_sexo = (('F', 'Feminino'),
                    ('M', 'Maculino'))
    nome = models.CharField(max_length=50)
    sobrenome = models.CharField(max_length=50, null=True, blank=True)
    cpf = models.CharField(max_length=14, unique=True, blank=True, null=True)
    sexo = models.CharField(max_length=1, choices=choices_sexo)
    idade = models.IntegerField()
    email = models.EmailField()
    telefone = models.CharField(max_length=19)
    nutri = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome
    
class DadosPaciente(models.Model):
    paciente = models.ForeignKey(Pacientes, on_delete=models.CASCADE)
    data = models.DateTimeField()
    peso = models.IntegerField()
    altura = models.IntegerField()
    taxa_metabolismo_basal = models.IntegerField(blank=True, null=True)
    percentual_gordura = models.IntegerField()
    percentual_musculo = models.IntegerField()
    colesterol_hdl = models.IntegerField()
    colesterol_ldl = models.IntegerField()
    colesterol_total = models.IntegerField()
    trigliceridios = models.IntegerField()


    def __str__(self):
        return f"Paciente({self.paciente.nome}, {self.peso})"
    
class Refeicao(models.Model):
    paciente = models.ForeignKey(Pacientes, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=50)
    horario = models.TimeField()
    carboidratos = models.IntegerField()
    proteinas = models.IntegerField()
    gorduras = models.IntegerField()

    def __str__(self):
        return f'{self.titulo} {self.paciente.nome}' 

class Opcao(models.Model):
    refeicao = models.ForeignKey(Refeicao, on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to="opcao", null=True, blank=True)
    descricao = models.TextField()

    def __str__(self):
        return self.refeicao.titulo + ' ' + self.refeicao.paciente.nome

class GeraDados(models.Model):
    nutri = models.ForeignKey(User, on_delete=models.CASCADE)
    limite = models.IntegerField(default=40)

    def __str__(self):
        return self.nutri.username

    
