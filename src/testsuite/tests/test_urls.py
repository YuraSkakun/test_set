from django.core.management import call_command
from django.urls import reverse
from django.test import TestCase
from django.test import Client


class UrlsAvailabilityTests(TestCase):

    def setUp(self):
        call_command('loaddata', 'tests/fixtures/accounts.json', verbosity=0)
        self.client = Client()

    def test_public_url(self):
        urls = [
            # ('', 'Welcome to TestSuite!'),
            (reverse('index'), 'Welcome to TestSuite!'),
            (reverse('testsuite:list'), 'Test Suites'),
        ]
        for url, content in urls:
            response = self.client.get(url)
            assert response.status_code == 200
            assert content in response.content.decode()  # decode bytestring

    def test_private_urls(self):
        private_urls = [
            # reverse('testsuite:list'),
            reverse('testsuite:leader_board'),
        ]
        for url in private_urls:
            response = self.client.get(url)
            print(response.url, type(response.url))  # /account/login/?next=/testsuite/leader/ <class 'str'>
            # '/account/login/?next=/testsuite/leader/'
            print(reverse('account:login'))  # /account/login/
            # assert response.status_code == 302
            self.assertEqual(response.status_code, 302)
            assert response.url.startswith(reverse('account:login'))
            # self.assertRedirects(response, '{}?next={}'.format('/account/login/', url))
            self.assertRedirects(response, '{}?next={}'.format(reverse('account:login'), url))

    def test_authorized_urls(self):
        # call_command('loaddata', 'tests/fixtures/accounts.json', verbosity=0)
        # self.client.login(username='admin', password='admin')
        self.client.login(username='admin', password='o...')

        auth_urls = [
            # (reverse('testsuite:leader_board'), 'Leader Board'),
            ('/testsuite/leader/', 'Leader Board')
        ]
        for url, content in auth_urls:
            response = self.client.get(url)
            # print(response.status_code)
            # assert response.status_code == 302
            assert response.status_code == 200
            # print(response.content.decode())
            assert content in response.content.decode()
