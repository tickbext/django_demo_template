from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from first.models import CalcHistory


class IndexTest(TestCase):
    def setUp(self):
        c = Client()
        self.response = c.get(reverse('index'))

    def test_index_response(self):
        self.assertEqual(self.response.status_code, 200)

    def test_index_context(self):
        self.assertEqual(self.response.context['pages'], 3)
        self.assertEqual(self.response.context['auth'], 'Andrew')
        self.assertTrue('cr_date' in self.response.context)


class CalculatorTest(TestCase):
    fixtures = ['test_database.json']   # manage.py dumpdata to get it

    def setUp(self):
        # self.client = Client(enforce_csrf_checks=True)                  # Для проверки csrf-токенов
        self.client = Client()
        self.user = User.objects.get(username='test_user')
        # self.client.login(username='test_user', password='promprog')    # для проверки авторизации
        self.client.force_login(user=self.user)                         # для быстрой авторизации

    def auth_protection(self):
        unauth_client = Client()
        response = unauth_client.get(reverse('calc'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        # response = unauth_client.get(reverse('calc'), follow=True)
        # self.assertEqual(response.status_code, 200)
        # last_url, status_code = response.redirect_chain[-1]    # если нужно отследить цепочку редиректов
        # self.assertIn(reverse('login'), last_url)

    def test_simple_get(self):
        response = self.client.get(reverse('calc'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertTrue('Калькулятор' in response.context['pagename'])

    def test_simple_post(self):
        response = self.client.post(reverse('calc'), {'first': 1, 'second': 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['first_value'], '1')
        self.assertEqual(response.context['second_value'], '2')
        self.assertEqual(response.context['result'], 3)

    def test_invalid_post(self):
        response = self.client.post(reverse('calc'), {'first': 'ahaha', 'second': 'ehehe'})
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.context['form'].errors), 0)
        self.assertFormError(response, 'form', 'first', 'Enter a whole number.')

    def test_empty_post(self):
        response = self.client.post(reverse('calc'), {})
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.context['form'].errors), 0)

    def test_history(self):
        response = self.client.post(reverse('calc'), {'first': 366, 'second': 768})
        history_item = response.context['history'].last()
        self.assertEqual(history_item.author, self.user)
        self.assertEqual(history_item.first, 366)
        self.assertEqual(history_item.second, 768)
        self.assertEqual(history_item.result, 1134)

    def test_empty_history(self):
        CalcHistory.objects.all().delete()
        response = self.client.get(reverse('calc'))
        self.assertContains(response, 'Нет данных')

