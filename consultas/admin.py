from django.contrib import admin
from . models import Consulta, DadosConsulta, CodigoPedido, Cancelamento

admin.site.register(Consulta)
admin.site.register(DadosConsulta)
admin.site.register(CodigoPedido)
admin.site.register(Cancelamento)