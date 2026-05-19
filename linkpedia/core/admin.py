from django.contrib import admin
from .models import LinkModel # Importe o seu model

# Registra o model no painel Admin
admin.site.register(LinkModel)