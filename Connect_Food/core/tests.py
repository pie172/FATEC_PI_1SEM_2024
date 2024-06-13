from django.test import TestCase, Client
from django.urls import reverse

class ViewTests(TestCase):
    def test_index_page_status_code(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_doar_alimento_response(self):
        form_data = {
            'nome': 'John Doe',
            'cpf': '12345678901',
            'cnpj': '12345678901234',
            'email': 'johndoe@example.com',
            'telefone': '11999999999',
            'endereco': '1234 Main St',
            'horario': '10:00',
            'alimento_id': 1,
            'categoria': 'Frutas',
            'alimento': 'Maçã',
            'quantidade': 10,
            'quant_medida': 'Kg',
            'validade': '2024-12-31'
        }
        response = self.client.post(reverse('doar_alimento'), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'doar_alimento.html')
        self.assertIn('True', response.context)

    def test_template_used(self):
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'index.html')

    def test_context_data(self):
        response = self.client.get(reverse('index'))

    def test_form_submission(self):
        form_data = {
            'nome': 'Jane Doe',
            'cpf': '98765432101',
            'email': 'janedoe@example.com',
            'telefone': '11998887777',
            'endereco': '1234 Main St',
            'horario': '10:00',
            'alimento_id': 2,
            'categoria': 'Vegetais',
            'alimento': 'Cenoura',
            'quantidade': 5,
            'quant_medida': 'Kg',
            'validade': '2024-06-30'
        }
        response = self.client.post(reverse('doar_alimento'), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'doar_alimento.html')
        self.assertIn('True', response.context)
