from django.contrib import admin
from . models import Pacientes, DadosPaciente, Refeicao, Opcao, GeraDados

@admin.register(Pacientes)
class PacientesAdmin(admin.ModelAdmin):
    list_display = ['nome', 'nutri', ]


@admin.register(GeraDados)
class GeradadosAdmin(admin.ModelAdmin):
    list_display = ['nutri', 'limite']

admin.site.register(Refeicao)
admin.site.register(Opcao)
admin.site.register(DadosPaciente)

