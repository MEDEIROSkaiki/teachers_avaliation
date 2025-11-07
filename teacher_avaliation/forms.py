# Em seu_app/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Pessoa
from .models import Disciplina, Pessoa

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
    
class DisciplinaForm(forms.ModelForm):
    class Meta:
        model = Disciplina  # Baseado no modelo de Disciplina
        fields = ['nome', 'codigo', 'data_inicio'] # Campos que você quer exibir

        # (Opcional) Se você quiser usar widgets do bootstrap, etc.
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'data_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

# ==========================================================
# 1. FORMULÁRIO DE CRIAÇÃO (PARA TELA DE SIGNUP)
#    Isto é o que vai fazer seu signup.html funcionar.
# ==========================================================
class PessoaCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Pessoa
        # Coloque os campos que o usuário deve preencher ao se cadastrar
        # O Django cuida dos campos de senha automaticamente
        fields = ('cpf', 'nome', 'data_nascimento', 'tipo')

    # (Opcional) Você pode estilizar os campos aqui também, como fez no login
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control'
        
        # Exemplo de placeholder
        self.fields['cpf'].widget.attrs['placeholder'] = 'Digite apenas números'


# ==========================================================
# 2. (BÔNUS) FORMULÁRIO DE MUDANÇA (PARA A ÁREA ADMIN)
#    Você vai precisar disso para o seu /admin funcionar
# ==========================================================
class PessoaChangeForm(UserChangeForm):
    class Meta:
        model = Pessoa
        # Defina os campos que podem ser editados no /admin
        fields = ('cpf', 'nome', 'data_nascimento', 'tipo', 'is_active', 'is_staff')