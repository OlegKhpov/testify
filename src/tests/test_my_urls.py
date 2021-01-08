from django.test import TestCase
from django.test import Client
from django.urls import reverse

from testify.models import Test


class TestUrls(TestCase):
    fixtures = [
        'tests/fixtures/dump.json',
    ]

    def setUp(self):
        self.client = Client()
        self.client.login(username='admin', password='admin')
        self.test_obj = Test.objects.all().first()

    def test_index(self):
        response = self.client.get(reverse('testify:index'))
        self.assertEqual(response.status_code, 200)

    def test_details(self):
        response = self.client.get(reverse('testify:test', kwargs={'uuid': self.test_obj.uuid}))
        self.assertEqual(response.status_code, 200)

    def test_user_page(self):
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 200)

    def test_leaderboard(self):
        response = self.client.get(reverse('testify:leaderboard'))
        self.assertEqual(response.status_code, 200)

    def test_contact_us(self):
        response = self.client.get(reverse('accounts:contact_us'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('accounts:contact_us'), {
            'subject': 'test_autoemail',
            'message': 'test-test-test',
        })
        self.assertEqual(response.status_code, 302)
        response = self.client.post(reverse('accounts:contact_us'))
        self.assertEqual(response.status_code, 200)

    def test_restart(self):
        response = self.client.get(reverse('testify:start', kwargs={'uuid': self.test_obj.uuid}))
        response = self.client.get(reverse('testify:index'))
        response = self.client.get(reverse('testify:start', kwargs={'uuid': self.test_obj.uuid}))
        self.assertEqual(response.status_code, 302)
        self.client.get(reverse('testify:restart', kwargs={'uuid': self.test_obj.uuid}))
        self.assertEqual(response.status_code, 302)
