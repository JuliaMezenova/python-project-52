from django.test import TestCase, Client
from django.urls import reverse
from task_manager.users.models import User
from django.utils.translation import gettext as _
from django.contrib.messages import get_messages


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
    fixtures = ["users.json"]

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
        new_user = User.objects.last()
        self.assertEqual(self.user['last_name'], new_user.last_name)


class UpdateUserTest(TestCase):
    fixtures = ["users.json"]

    def setUp(self):
        self.client = Client()
        self.user71 = User.objects.get(pk=71)
        self.user72 = User.objects.get(pk=72)
        self.form_data = {
            'first_name': 'Test',
            'last_name': 'Testov',
            'username': 'TestTestovich',
            'password1': 'SecretPass555',
            'password2': 'SecretPass555',
        }

    def test_update_user(self):
        self.client.force_login(self.user71)
        update_url = reverse('user_update', args=[self.user71.pk])
        get_response = self.client.get(update_url)
        self.assertEqual(get_response.status_code, 200)
        post_response = self.client.post(update_url, self.form_data)
        self.user71.refresh_from_db()
        self.assertRedirects(post_response, reverse('users_index'), 302, 200)
        updated_user = User.objects.get(pk=71)
        self.assertEqual(updated_user.username, 'TestTestovich')
        messages = list(get_messages(post_response.wsgi_request))
        self.assertEqual(len(messages), 1)
        content = post_response.content.decode()
        self.assertNotIn('TestTestov', content)
        # self.assertIn(_("The user has been successfully changed"), content)

    def test_update_user_without_perm(self):
        self.client.force_login(self.user71)
        self.update_url = reverse('user_update', args=[self.user72.pk])
        response = self.client.get(self.update_url)
        self.assertRedirects(response, reverse('users_index'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)


class DeleteUserTest(TestCase):
    fixtures = ["users.json"]

    def setUp(self):
        self.client = Client()
        self.user71 = User.objects.get(pk=71)
        self.user72 = User.objects.get(pk=72)

    def test_delete_user(self):
        self.client.force_login(self.user71)
        self.delete_url = reverse('user_delete', args=[self.user71.pk])
        self.client.get(self.delete_url)
        response = self.client.post(self.delete_url, follow=True)
        self.assertRedirects(response, reverse('users_index'), 302, 200)
        content = response.content.decode()
        self.assertIn(_("The user has been successfully deleted"), content)
        self.assertNotIn('TestTestov', content)

    def test_delete_user_without_perm(self):
        self.client.force_login(self.user71)
        self.delete_url = reverse('user_delete', args=[self.user72.pk])
        response = self.client.get(self.delete_url)
        self.assertRedirects(response, reverse('users_index'), 302, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)


class MyTest(TestCase):
    fixtures = ["users.json"]

    def test_should_create_user(self):
        user = User.objects.get(pk=72)
        self.assertEqual(user.username, "Cheburashka")
