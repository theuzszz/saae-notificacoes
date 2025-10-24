# notificacoes/views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from .models import Bairro, Evento, Assinante, LogEnvio
from .forms import AssinaturaForm


# --- Páginas públicas básicas ---

def home(request):
    bairros = Bairro.objects.filter(ativo=True).order_by('nome')
    return render(request, 'home.html', {'bairros': bairros})


def eventos_por_bairro(request, bairro_id):
    bairro = get_object_or_404(Bairro, pk=bairro_id, ativo=True)
    agora = timezone.now()
    eventos = Evento.objects.filter(bairro=bairro).order_by('-inicio_previsto')
    return render(request, 'eventos.html', {'bairro': bairro, 'eventos': eventos, 'agora': agora})


def assinar(request):
    if request.method == 'POST':
        form = AssinaturaForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'assinar_ok.html')
    else:
        form = AssinaturaForm()
    return render(request, 'assinar.html', {'form': form})


def api_eventos_por_bairro(request, bairro_id):
    eventos = (
        Evento.objects
        .filter(bairro_id=bairro_id)
        .order_by('-inicio_previsto')
        .values('id', 'titulo', 'descricao', 'inicio_previsto', 'fim_previsto', 'status')
    )
    return JsonResponse(list(eventos), safe=False)


# --- Relatórios (F8) ---

def _to_date(value):
    """Converte 'YYYY-MM-DD' em date ou retorna None."""
    try:
        from datetime import datetime
        return datetime.strptime(value, '%Y-%m-%d').date()
    except Exception:
        return None


def relatorios(request):
    """
    Relatório de envios com filtro por período/status/canal/tipo.
    Se ?export=csv, exporta os resultados.
    """
    de = request.GET.get('de')         # 'YYYY-MM-DD'
    ate = request.GET.get('ate')       # 'YYYY-MM-DD'
    status = request.GET.get('status') # status do Evento
    canal = request.GET.get('canal')   # email|sms|whatsapp
    tipo = request.GET.get('tipo')     # alerta|normalizacao

    qs = LogEnvio.objects.select_related('evento', 'evento__bairro')

    if de and _to_date(de):
        qs = qs.filter(data_envio__date__gte=de)
    if ate and _to_date(ate):
        qs = qs.filter(data_envio__date__lte=ate)
    if status:
        qs = qs.filter(evento__status=status)
    if canal:
        qs = qs.filter(canal=canal)
    if tipo:
        qs = qs.filter(tipo=tipo)

    # Exportar CSV
    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="relatorio_envios.csv"'
        import csv
        writer = csv.writer(response)
        writer.writerow(['Data envio', 'Bairro', 'Evento', 'Tipo', 'Canal', 'Destinatário', 'Sucesso'])
        for log in qs.order_by('-data_envio'):
            writer.writerow([
                log.data_envio.strftime('%Y-%m-%d %H:%M:%S'),
                log.evento.bairro.nome,
                log.evento.titulo,
                log.tipo,
                log.canal,
                log.destinatario,
                'OK' if log.sucesso else 'Falha',
            ])
        return response

    # Página HTML
    context = {
        'logs': qs.order_by('-data_envio')[:500],  # limita para não pesar
        'filtros': {
            'de': de or '', 'ate': ate or '', 'status': status or '', 'canal': canal or '', 'tipo': tipo or ''
        }
    }
    return render(request, 'relatorios.html', context)
