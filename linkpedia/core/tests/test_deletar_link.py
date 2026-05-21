from django.test import TestCase
from django.urls import reverse
from core.models import LinkModel

class ExclusaoLinkTest(TestCase):
    def setUp(self):
        self.link = LinkModel.objects.create(
            titulo="Link a ser deletado",
            link="https://deletar.com"
        )
        self.url = reverse('deletar', args=[self.link.id])

    def test_view_deleta_o_link_do_banco_e_redireciona(self):
        """Testa se a função apaga o item e volta para a lista"""
        self.assertEqual(LinkModel.objects.count(), 1)
        
        response = self.client.get(self.url)
        
        self.assertRedirects(response, reverse('listar'))
        
        self.assertEqual(LinkModel.objects.count(), 0)

    def test_deletar_id_inexistente_retorna_erro_404(self):
        """Testa a proteção do get_object_or_404 na exclusão"""
        url_invalida = reverse('deletar', args=[999])
        response = self.client.get(url_invalida)
        
        self.assertEqual(response.status_code, 404)