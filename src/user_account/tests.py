from django.test import TestCase

# Create your tests here.
from django.core.management import call_command
from django.urls import reverse
from django.test import Client


class UrlsAvailabilityTests(TestCase):

    def setUp(self):
        call_command('loaddata', 'tests/fixtures/accounts.json', verbosity=0)

        self.client = Client()

    def test_public_url(self):

        urls = [
            (reverse('account:registration'), 'Register new user'),
            (reverse('account:login'), 'Login as a user'),
        ]
        for url, content in urls:
            response = self.client.get(url)
            assert response.status_code == 200
            assert content in response.content.decode()

    def test_private_urls(self):

        private_urls = [
            reverse('account:profile'),
            reverse('account:logout'),

        ]
        for url in private_urls:
            response = self.client.get(url)
            self.assertRedirects(response, '{}?next={}'.format(reverse('account:login'), url))

    def test_auth_user_urls(self):

        self.client.login(username='admin', password='o...')

        private_urls = [
            (reverse('account:profile'), 'Edit current user profile'),
            (reverse('account:logout'), 'Logout from TESTS'),

        ]
        for url, content in private_urls:
            response = self.client.get(url)
            assert response.status_code == 200
            assert content in response.content.decode()


'''
from user_account.models import User

CREDENTIALS = {
    'username': 'AdminUser',
    'first_name': 'AdminUserFirst',
    'last_name': 'AdminUserLast',
    'email': 'email@admin.com',
    'password1': 'FhTy123@#$%',
    'password2': 'FhTy123@#$%',
}


class RegistrationTests(TestCase):

    def setUp(self):
        self.client = Client()

    def _register(self, credentials):
        url = reverse('account:registration')
        return self.client.post(url, credentials)

    def test_registration(self):
        users_count = User.objects.count()
        response = self._register(CREDENTIALS)
        assert response.url.startswith(reverse('account:login'))
        assert response.status_code == 302
        assert User.objects.count() == (users_count + 1)

    def test_login(self):
        self._register(CREDENTIALS)
        self.client.login(username='AdminUser', password='FhTy123@#$%')
        response = self.client.get(reverse('account:profile'))
        assert response.status_code == 200
        # print(response.content.decode())
        # assert 'Update' in response.content.decode()
        assert 'Edit current user profile' in response.content.decode()
'''
