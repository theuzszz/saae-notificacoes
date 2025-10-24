# notificacoes/admin.py
from django.contrib import admin
from .models import Bairro, Assinante, Evento, LogEnvio

@admin.register(Bairro)
class BairroAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'ativo')
    search_fields = ('nome',)
    list_filter = ('ativo',)

@admin.register(Assinante)
class AssinanteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'email', 'telefone', 'bairro', 'ativo')
    search_fields = ('nome', 'email', 'telefone')
    list_filter = ('ativo', 'bairro')

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'bairro', 'inicio_previsto', 'fim_previsto', 'status')
    list_filter = ('status', 'bairro')
    search_fields = ('titulo', 'descricao')
    date_hierarchy = 'inicio_previsto'

@admin.register(LogEnvio)
class LogEnvioAdmin(admin.ModelAdmin):
    list_display = ('id', 'evento', 'destinatario', 'canal', 'tipo', 'data_envio', 'sucesso', 'tentativa')
    list_filter = ('canal', 'tipo', 'sucesso')
    search_fields = ('destinatario',)
    date_hierarchy = 'data_envio'