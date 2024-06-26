from django.urls import path
from . import views

urlpatterns = [
    path('pacientes/', views.pacientes, name='pacientes'),
    path('pacientes_filter/', views.pacientes_filter, name='pacientes_filter'),
    path('', views.dashboard, name='dashboard'),
    path('dados_paciente/<str:id>/', views.dados_paciente, name="dados_paciente"),
    path('atualiza_dados_paciente/<str:id>/', views.atualiza_dados_paciente, name="atualiza_dados_paciente"),
    path('grafico_peso/<str:id>/', views.grafico_peso, name="grafico_peso"),
    path('plano_alimentar_listar/', views.plano_alimentar_listar, name="plano_alimentar_listar"),
    path('plano_alimentar/<str:id>/', views.plano_alimentar, name="plano_alimentar"),
    path('plano_alimentar_filter/', views.plano_alimentar_filter, name="plano_alimentar_filter"),
    path('edita_refeicao/<str:id_paciente>/', views.edita_refeicao, name="edita_refeicao"),
    path('edita_opcao/<str:id_paciente>/', views.edita_opcao, name="edita_opcao"),
    path('exclui_refeicao/<str:id_paciente>/', views.exclui_refeicao, name="exclui_refeicao"),
    path('exclui_opcao/<str:id_paciente>/', views.exclui_opcao, name="exclui_opcao"),
    path('refeicao/<str:id_paciente>/', views.refeicao, name="refeicao"),
    path('opcao/<str:id_paciente>/', views.opcao, name="opcao"),
    path('pacientes/editar/<str:id>/', views.pacientes_editar, name="pacientes_editar"),
    path('pacientes/excluir/<str:id>/', views.pacientes_excluir, name="pacientes_excluir"),
    path('gerar_dados', views.gerar_dados, name='gerar'),
    path('gerar_dados/tudo/', views.gerar_tudo, name="gerar_tudo"),
]
