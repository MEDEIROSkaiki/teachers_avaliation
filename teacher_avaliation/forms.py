# Em seu_app/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

class LoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': _(
            "Por favor, digite um CPF e senha corretos. Note que ambos os "
            "campos diferenciam maiúsculas de minúsculas."
        ),
        'inactive': _("Esta conta está inativa."),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Digite seu CPF (apenas números)'}
        )
        self.fields['username'].label = 'CPF'

        self.fields['password'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Digite sua senha'}
        )
        self.fields['password'].label = 'Senha'

    def clean(self):
        # A lógica de validação permanece a mesma do AuthenticationForm,
        # mas agora usará nossas mensagens de erro personalizadas.
        return super().clean()