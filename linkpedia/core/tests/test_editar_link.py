from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from core.models import LinkModel

User = get_user_model()

class EdicaoLinkTest(TestCase):
    def setUp(self):
        # Cria e loga o usuário
        self.user = User.objects.create_user(
            username='alunoteste',
            email='teste@cps.sp.gov.br',
            password='senha_secreta'
        )
        self.client.force_login(self.user)
        
        # Cria o link para testar
        self.link = LinkModel.objects.create(
            titulo="Google",
            link="https://google.com",
            observacao="Buscador original"
        )   
        self.url = reverse('editar', args=[self.link.id])

    def test_acesso_carrega_form_preenchido_com_dados_antigos(self):
        """Teste de GET: Verifica se a página abre e envia o form com a instance correta"""
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edita_links.html')
        
        # Garante que o form no HTML está preenchido com o objeto correto
        form_enviado = response.context['form']
        self.assertEqual(form_enviado.instance, self.link)

    def test_post_atualiza_dados_no_banco_e_redireciona(self):
        """Teste de POST: Envia dados novos e verifica se alterou no banco"""
        dados_novos = {
            'titulo': 'Google Editado',
            'link': 'https://google.com.br',
            'observacao': 'Buscador atualizado'
        }
        
        response = self.client.post(self.url, dados_novos)
        
        # Verifica se redirecionou para a página 'listar'
        self.assertRedirects(response, reverse('listar'))
        
        # Atualiza o objeto self.link com o que está no banco agora
        self.link.refresh_from_db()
        
        # Verifica se o título realmente mudou
        self.assertEqual(self.link.titulo, 'Google Editado')
        self.assertEqual(self.link.link, 'https://google.com.br')

    def test_editar_id_inexistente_retorna_erro_404(self):
        """Testa a proteção do get_object_or_404"""
        url_invalida = reverse('editar', args=[999]) # ID que não existe
        response = self.client.get(url_invalida)
        
        self.assertEqual(response.status_code, 404)