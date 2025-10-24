# saae/urls.py
from django.contrib import admin
from django.urls import path
from notificacoes import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('bairros/<int:bairro_id>/', views.eventos_por_bairro, name='eventos_por_bairro'),
    path('assinar/', views.assinar, name='assinar'),
    path('api/bairros/<int:bairro_id>/eventos/', views.api_eventos_por_bairro, name='api_eventos_por_bairro'),
    path('relatorios/', views.relatorios, name='relatorios'),


]