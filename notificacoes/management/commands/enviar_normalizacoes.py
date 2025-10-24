from django.core.management.base import BaseCommand
from notificacoes.models import Evento, Assinante, LogEnvio


class Command(BaseCommand):
    help = 'Envia notificação de normalização quando status for "normalizado"'

    def handle(self, *args, **options):
        eventos = Evento.objects.filter(status='normalizado')
        for ev in eventos:
            assinantes = Assinante.objects.filter(bairro=ev.bairro, ativo=True)
            for a in assinantes:
                contato = a.email or a.telefone
                if not contato:
                    continue
                if LogEnvio.objects.filter(evento=ev, destinatario=contato, tipo='normalizacao', sucesso=True).exists():
                    continue
                msg = f'Normalização: "{ev.titulo}" em {ev.bairro.nome} foi normalizado.'
                print(f'-> {contato}: {msg}')
                LogEnvio.objects.create(
                    evento=ev, destinatario=contato,
                    canal='email' if a.email else 'sms',
                    sucesso=True, tipo='normalizacao'
                )