
from django.db import models

class Bairro(models.Model):
    nome = models.CharField(max_length=120, unique=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return self.nome

class Assinante(models.Model):
    nome = models.CharField(max_length=120)
    email = models.EmailField(blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    bairro = models.ForeignKey(Bairro, on_delete=models.PROTECT, related_name='assinantes')
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.nome} ({self.bairro})'

class Evento(models.Model):
    STATUS = [
        ('planejado', 'Planejado'),
        ('em_andamento', 'Em andamento'),
        ('normalizado', 'Normalizado'),
        ('cancelado', 'Cancelado'),
    ]
    titulo = models.CharField(max_length=140)
    descricao = models.TextField(blank=True)
    bairro = models.ForeignKey(Bairro, on_delete=models.PROTECT, related_name='eventos')
    inicio_previsto = models.DateTimeField()
    fim_previsto = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS, default='planejado')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=['bairro', 'inicio_previsto', 'status'])]
        ordering = ['-inicio_previsto']

    def __str__(self):
        return f'{self.titulo} - {self.bairro} ({self.status})'

class LogEnvio(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='logs')
    destinatario = models.CharField(max_length=255)  # email ou telefone
    canal = models.CharField(max_length=30)          # 'email' | 'sms' | 'whatsapp'
    data_envio = models.DateTimeField(auto_now_add=True)
    sucesso = models.BooleanField(default=False)
    tentativa = models.PositiveIntegerField(default=1)
    tipo = models.CharField(max_length=20, default='alerta')  # 'alerta' | 'normalizacao'

    class Meta:
        indexes = [
            models.Index(fields=['evento', 'destinatario', 'tipo']),
        ]
        unique_together = [('evento', 'destinatario', 'tipo', 'tentativa')]

    def __str__(self):
        return f'{self.evento_id} -> {self.destinatario} ({self.tipo})'