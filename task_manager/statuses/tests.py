from django.test import TestCase, Client
from ..users.models import User
from .models import Status
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _


class StatusTest(TestCase):
    fixtures = ["statuses.json", "users.json"]

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(pk=71)
        self.client.force_login(self.user)
        self.form_data = {
            'create': {'name': 'New status'},
            'update': {'name': 'Updated status'},
        }
        self.status1 = Status.objects.get(pk=1)
        self.status2 = Status.objects.get(pk=2)
        self.status3 = Status.objects.get(pk=3)
        self.statuses_list = reverse('statuses_index')

    def test_create_status(self):
        create_url = reverse('status_create')
        get_response = self.client.get(create_url)
        self.assertEqual(get_response.status_code, 200)
        post_response = self.client.post(create_url, self.form_data['create'], follow=True)
        self.assertRedirects(post_response, self.statuses_list)
        self.assertTrue(Status.objects.get(pk=4))
        content = post_response.content.decode()
        self.assertIn('New status', content)
        self.assertContains(post_response, _("Status successfully created"))

    def test_update_status(self):
        update_url = reverse('status_update', args=[self.status1.pk])
        get_response = self.client.get(update_url)
        self.assertEqual(get_response.status_code, 200)
        post_response = self.client.post(update_url, self.form_data['update'], follow=True)
        self.assertRedirects(post_response, self.statuses_list)
        self.assertTrue(Status.objects.get(pk=1))
        content = post_response.content.decode()
        self.assertIn('Updated status', content)
        self.assertContains(post_response, _("Status successfully changed"))

    def test_delete_not_used_status(self):
        delete_url = reverse('status_delete', args=[2])
        get_response = self.client.get(delete_url)
        self.assertEqual(get_response.status_code, 200)
        post_response = self.client.post(delete_url, follow=True)
        self.assertRedirects(post_response, self.statuses_list)
        self.assertEqual(len(Status.objects.all()), 2)
        content = post_response.content.decode()
        self.assertNotIn('On Testing', content)
        self.assertContains(post_response, _("Status successfully deleted"))

    def test_read_status(self):
        get_response = self.client.get(self.statuses_list)
        content = get_response.content.decode()
        self.assertIn(self.status1.name, content)
        self.assertIn(self.status3.name, content)


class MyTest(TestCase):
    fixtures = ["statuses.json"]

    def test_should_create_status(self):
        status = Status.objects.get(pk=3)
        self.assertEqual(status.name, "New")
