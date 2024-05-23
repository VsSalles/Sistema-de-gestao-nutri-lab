from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('agenda/', views.agenda, name='agenda'),
    path('agenda/filter/', views.agenda_filter, name='agenda_filter'),
    path('realizar/<str:pedido>/', views.realizar, name='realizar'),
    path('detalhes/<str:pedido>/', views.detalhes, name='detalhes'),
    path('cancelar/<str:pedido>/', views.cancelar, name='cancelar'),
    path('motivo/<str:pedido>/', views.motivo_cancelamento, name='motivo'),
    path('comprovante/<str:pedido>/', views.comprovante, name='comprovante'),
    path('gera_pdf/<str:pedido>/', views.gera_pdf, name='pdf'),



]