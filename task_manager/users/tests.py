from django.test import TestCase, Client
from django.urls import reverse
from task_manager.users.models import User
from django.utils.translation import gettext as _


class SimpleTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index(self):
        response = self.client.get('/')
        status_code = response.status_code
        self.assertEqual(status_code, 200)

        content = response.content.decode()
        self.assertIn(_('Hello from Hexlet!'), content)
        self.assertIn(_('Sign Up'), content)
        self.assertIn('href="https://ru.hexlet.io">Hexlet</a>', content)


class CreateUserTest(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('user_create')
        self.empty_form = {
            'first_name': '',
            'last_name': '',
            'username': '',
            'password1': '',
            'password2': '',
        }
        self.user = {
            'first_name': 'Name',
            'last_name': 'Surname',
            'username': 'User1',
            'password1': 'SecretPass123',
            'password2': 'SecretPass123',
        }
        self.user_with_short_password = {
            'first_name': 'Name',
            'last_name': 'Surname',
            'username': 'User1',
            'password1': 'Se',
            'password2': 'Se',
        }
        self.user_with_invalid_username = {
            'first_name': 'Name',
            'last_name': 'Surname',
            'username': 'User1#',
            'password1': 'SecretPass123',
            'password2': 'SecretPass123',
        }
        return super().setUp()

    def test_can_view_page_correctly(self):
        response = self.client.get(self.register_url)
        status_code = response.status_code
        self.assertEqual(status_code, 200)
        self.assertTemplateUsed(response, 'users/create.html')

    def test_empty_form(self):
        response = self.client.post(self.register_url, self.empty_form)
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_can_register_user(self):
        response = self.client.post(self.register_url, self.user)
        status_code = response.status_code
        self.assertEqual(status_code, 302)

    def test_cant_register_user_with_short_password(self):
        response = self.client.post(self.register_url, self.user_with_short_password)
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_cant_register_user_with_invalid_username(self):
        response = self.client.post(self.register_url, self.user_with_invalid_username)
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_cant_register_user_with_taken_username(self):
        self.client.post(self.register_url, self.user)
        response = self.client.post(self.register_url, self.user)
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_create_user(self):
        self.login = reverse('login')
        response = self.client.post(self.register_url, self.user, follow=True)
        self.assertRedirects(response, self.login)
        self.assertTrue(User.objects.get(pk=70))
        content = response.content.decode()
        self.assertIn(_('The user successfully created'), content)


class UpdateUserTest(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.client = Client()
        self.user68 = User.objects.get(pk=68)
        self.user69 = User.objects.get(pk=69)

    def test_update_user(self):
        self.client.force_login(self.user68)
        self.update_url = reverse('user_update', args=[68])
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(self.update_url, {'username': 'TestTestovich'}, follow=True)
        self.assertEqual(response.status_code, 302)
        self.user68.refresh_from_db()
        self.assertEqual(self.user68.username, 'TestTestovich')
        content = response.content.decode()
        self.assertIn(_('The user successfully updated'), content)

    def test_can_view_page_correctly(self):
        self.update_url = reverse('user_update', args=[self.user68.pk])
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/update.html')

    def test_update_user_without_perm(self):
        self.client.force_login(self.user68)
        self.update_url = reverse('user_update', args=[self.user69.pk])
        response = self.client.get(self.update_url)
        self.assertRedirects(response, reverse('users_index'))
        content = response.content.decode()
        self.assertIn(_('You do not have the rights to change another user.'), content)


class DeleteUserTest(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.client = Client()
        self.user68 = User.objects.get(pk=68)
        self.user69 = User.objects.get(pk=69)

    def test_delete_user(self):
        self.client.force_login(self.user68)
        self.delete_url = reverse('user_delete', args=[self.user68.pk])
        self.client.get(self.delete_url)
        response = self.client.post(self.delete_url, follow=True)
        self.assertRedirects(response, reverse('users_index'), 302, 200)
        content = response.content.decode()
        self.assertIn(_("The user has been successfully deleted"), content)
        self.assertNotIn('TestTestov', content)

    def test_delete_user_without_perm(self):
        self.client.force_login(self.user68)
        self.delete_url = reverse('user_delete', args=[self.user69.pk])
        response = self.client.get(self.delete_url)
        content = response.content.decode()
        self.assertIn(_("You do not have the rights to change another user."), content)
