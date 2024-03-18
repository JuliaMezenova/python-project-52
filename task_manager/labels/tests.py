from django.test import TestCase, Client
from ..users.models import User
from .models import Label
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _


class LabelTest(TestCase):
    fixtures = ["statuses.json", "users.json", "tasks.json", "labels.json"]

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.get(pk=1)
        self.client.force_login(self.user1)
        self.form_data = {
            'create': {'name': 'New label'},
            'update': {'name': 'Updated label'},
        }
        self.label1 = Label.objects.get(pk=1)
        self.label2 = Label.objects.get(pk=2)
        self.label3 = Label.objects.get(pk=3)
        self.label4 = Label.objects.get(pk=4)
        self.label5 = Label.objects.get(pk=5)
        self.labels_list = reverse('labels_index')

    def test_create_label(self):
        create_url = reverse('label_create')
        get_response = self.client.get(create_url)
        self.assertEqual(get_response.status_code, 200)
        post_response = self.client.post(create_url, self.form_data['create'], follow=True)
        self.assertRedirects(post_response, self.labels_list)
        self.assertTrue(Label.objects.get(pk=5))
        content = post_response.content.decode()
        self.assertIn('New label', content)
        self.assertContains(post_response, _("Label successfully created"))

    def test_update_label(self):
        update_url = reverse('label_update', args=[self.label3.pk])
        get_response = self.client.get(update_url)
        self.assertEqual(get_response.status_code, 200)
        post_response = self.client.post(update_url, self.form_data['update'], follow=True)
        self.assertRedirects(post_response, self.labels_list)
        self.assertTrue(Label.objects.get(pk=3))
        content = post_response.content.decode()
        self.assertIn('Updated label', content)
        self.assertContains(post_response, _("Label successfully changed"))

    def test_delete_used_label(self):
        delete_url = reverse('label_delete', args=[self.label2.pk])
        get_response = self.client.get(delete_url, follow=True)
        self.assertEqual(get_response.status_code, 200)
        post_response = self.client.post(delete_url, follow=True)
        self.assertRedirects(post_response, self.labels_list)
        self.assertEqual(len(Label.objects.all()), 5)
        content = post_response.content.decode()
        self.assertIn('Romashka', content)
        self.assertContains(post_response, _("It is not possible to delete a label because it is being used"))

    def test_delete_not_used_label(self):
        delete_url = reverse('label_delete', args=[self.label5.pk])
        get_response = self.client.get(delete_url)
        self.assertEqual(get_response.status_code, 200)
        post_response = self.client.post(delete_url, follow=True)
        self.assertRedirects(post_response, self.labels_list)
        self.assertEqual(len(Label.objects.all()), 4)
        content = post_response.content.decode()
        self.assertNotIn('Sunflower', content)
        self.assertContains(post_response, _("Label successfully deleted"))

    def test_read_label(self):
        get_response = self.client.get(self.labels_list)
        self.assertEqual(len(Label.objects.all()), 5)
        content = get_response.content.decode()
        self.assertIn(self.label1.name, content)
        self.assertIn(self.label2.name, content)
        self.assertIn(self.label3.name, content)
        self.assertIn(self.label4.name, content)
        self.assertIn(self.label5.name, content)


class MyTest(TestCase):
    fixtures = ["labels.json"]

    def test_should_create_label(self):
        label = Label.objects.get(pk=1)
        self.assertEqual(label.name, "Rose")
