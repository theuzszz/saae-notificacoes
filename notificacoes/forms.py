# notificacoes/forms.py
from django import forms
from .models import Assinante

class AssinaturaForm(forms.ModelForm):
    class Meta:
        model = Assinante
        fields = ['nome', 'email', 'telefone', 'bairro']

    def clean(self):
        cleaned = super().clean()
        email = cleaned.get('email')
        tel = cleaned.get('telefone')
        if not email and not tel:
            raise forms.ValidationError('Informe e-mail ou telefone.')
        return cleaned