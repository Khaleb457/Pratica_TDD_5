from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import LinkModel

class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ('email', 'password')
        labels = {
            'email': 'E-Mail:',
            'password': 'Senha:',
        }
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control',
                                             'placeholder':'Digite seu e-mail institucional'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control',
                                                   'placeholder':'Digite sua senha'}),
        }
        error_messages = {
            'email': {
                'required': ("Informe o e-mail."),
            },
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.endswith('@cps.sp.gov.br'):
            raise ValidationError('Informe seu e-mail institucional.')
        return self.cleaned_data['email']

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise ValidationError("Usuário com esse e-mail não encontrado.")

            user = authenticate(username=user.username, password=password)
            if user is None:
                raise ValidationError("Senha incorreta para o e-mail informado.")

            self.user = user

class LinkForm(forms.ModelForm):
    class Meta:
        model = LinkModel
        fields = ['titulo', 'link', 'observacao']
        
        # Utilizei Widgets para aplicar as classes do bootstrap diretamente no forms
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Google'}),
            'link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://www.exemplo.com'}),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Adicione uma observação...'}),
        }