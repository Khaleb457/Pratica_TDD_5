from django.test import TestCase
from django.urls import reverse
from core.models import LinkModel

class CadastroLinkTest(TestCase):
    def setUp(self):
        self.url = reverse('cadastro')

    def test_acesso_a_pagina_de_cadastro_retorna_status_200(self):
        """Teste se a página de cadastro carrega corretamente (GET)"""
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cadastro_link.html')

    def test_envio_de_formulario_salva_no_banco(self):
        """Teste se o envio de dados válidos cria um Link no banco (POST)"""
        data = {
            'titulo': 'Django Project',
            'link': 'https://www.djangoproject.com',
            'observacao': 'Site oficial do Django'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(LinkModel.objects.count(), 1)

        link_salvo = LinkModel.objects.first()
        self.assertEqual(link_salvo.titulo, 'Django Project')
        self.assertEqual(link_salvo.link, 'https://www.djangoproject.com')

    def test_representacao_em_string_do_model(self):
        """Teste para a função __str__ do LinkModel"""
        link = LinkModel.objects.create(
            titulo='Google',
            link='https://google.com'
        )
        self.assertEqual(str(link), 'Google - https://google.com')