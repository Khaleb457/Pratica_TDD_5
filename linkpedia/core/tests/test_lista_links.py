from django.test import TestCase
from django.urls import reverse
from core.models import LinkModel

class ListagemLinksTest(TestCase):
    def setUp(self):
        self.link1 = LinkModel.objects.create(
            titulo="Google",
            link="https://google.com",
            observacao="Buscador da web"
        )
        self.link2 = LinkModel.objects.create(
            titulo="Projeto Django",
            link="https://www.djangoproject.com",
            observacao="Site oficial do framework"
        )
        
        self.url = reverse('listar')

    def test_pagina_de_listagem_carrega_corretamente(self):
        """Teste se a página responde com status 200 e usa o template certo"""
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lista_links.html')

    def test_view_envia_variavel_links_para_o_template(self):
        """Teste se a View buscou os dados usando o .all() e mandou pro HTML"""
        response = self.client.get(self.url)
        
        # Verifica se a chave 'links' existe no dicionário (contexto) enviado ao template
        self.assertIn('links', response.context)
        
        # Pega a lista de itens que foi enviada e verifica se tem 2 itens
        links_enviados = response.context['links']
        self.assertEqual(len(links_enviados), 2)
        
        # Verifica se os links que criamos no setUp estão nessa lista
        self.assertIn(self.link1, links_enviados)
        self.assertIn(self.link2, links_enviados)
    
    def test_html_renderiza_os_titulos_na_tela(self):
        """Teste se os dados realmente viraram texto no HTML final (passaram pelo for)"""
        response = self.client.get(self.url)
        
        # O assertContains verifica se um texto específico existe dentro de todo o código HTML da página
        self.assertContains(response, "Google")
        self.assertContains(response, "Projeto Django")
        self.assertContains(response, "https://google.com")