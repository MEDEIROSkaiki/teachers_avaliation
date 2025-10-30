# Em seu_app/forms.py
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(
        label='Usuário',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',  # <-- ISSO APLICA O PADDING-LEFT
                'placeholder': 'Usuário'    # <-- ISSO MOSTRA O TEXTO-GUIA
            }
        )
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',  # <-- ISSO APLICA O PADDING-LEFT
                'placeholder': 'Senha'       # <-- ISSO MOSTRA O TEXTO-GUIA
            }
        )
    )