from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from notificacoes.models import Evento, Assinante, LogEnvio


def ja_enviado(evento, destinatario, tipo):
    return LogEnvio.objects.filter(evento=evento, destinatario=destinatario, tipo=tipo, sucesso=True).exists()


def enviar(canal, destinatario, msg):
    # Simulação/envio real: conecte email/SMS/WhatsApp aqui
    print(f'[{canal}] -> {destinatario}: {msg}')
    return True  # supondo sucesso


class Command(BaseCommand):
    help = 'Envia alertas 2 horas antes do início previsto'

    def handle(self, *args, **options):
        agora = timezone.now()
        janela_inicio = agora + timedelta(hours=2)
        eventos = Evento.objects.filter(
            status__in=['planejado', 'em_andamento'],
            inicio_previsto__gte=agora,
            inicio_previsto__lte=janela_inicio
        )

        for ev in eventos:
            assinantes = Assinante.objects.filter(bairro=ev.bairro, ativo=True)
            for a in assinantes:
                contato = a.email or a.telefone
                if not contato:
                    continue
                if ja_enviado(ev, contato, 'alerta'):
                    continue
                msg = f'Alerta: "{ev.titulo}" em {ev.bairro.nome} às {ev.inicio_previsto}.'
                ok = enviar('email' if a.email else 'sms', contato, msg)
                LogEnvio.objects.create(
                    evento=ev, destinatario=contato,
                    canal='email' if a.email else 'sms',
                    sucesso=ok, tipo='alerta'
                )