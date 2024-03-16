from django.test import TestCase, Client
from django.urls import reverse
from task_manager.users.models import User
from task_manager.tasks.models import Task
from django.utils.translation import gettext as _


class TaskTest(TestCase):
    fixtures = ["tasks.json", "statuses.json", "users.json"]

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
        self.user3 = User.objects.get(pk=3)
        self.form_data = {
            'create': {
                'name': 'To cook breakfast',
                'description': 'To cook sandvich',
                'status': 1,
                'executor': 1,
                'label': '',
            },
            'update': {
                'name': 'Make project number 4 UPDATE',
                'description': 'Updated PROJECT 4',
                'status': 3,
                'executor': 1,
                'label': '',
            }
        }
        self.task1 = Task.objects.get(pk=1)
        self.task2 = Task.objects.get(pk=2)
        self.task3 = Task.objects.get(pk=3)
        self.task4 = Task.objects.get(pk=4)
        self.tasks_list = reverse('tasks_index')

    def test_create_task(self):
        self.client.force_login(self.user1)
        create_url = reverse('task_create')
        get_response = self.client.get(create_url)
        self.assertEqual(get_response.status_code, 200)
        post_response = self.client.post(create_url, self.form_data['create'], follow=True)
        self.assertRedirects(post_response, self.tasks_list)
        self.assertTrue(Task.objects.get(pk=5))
        content = post_response.content.decode()
        self.assertIn('To cook breakfast', content)
        self.assertContains(post_response, _("Task successfully created"))

    def test_update_task(self):
        self.client.force_login(self.user1)
        update_url = reverse('task_update', args=[self.task1.pk])
        get_response = self.client.get(update_url)
        self.assertEqual(get_response.status_code, 200)
        post_response = self.client.post(update_url, self.form_data['update'], follow=True)
        self.assertRedirects(post_response, self.tasks_list)
        self.assertTrue(Task.objects.get(pk=1))
        content = post_response.content.decode()
        self.assertIn('Make project number 4 UPDATE', content)
        self.assertContains(post_response, _("Task successfully changed"))

    def test_delete_task_can_author(self):
        self.client.force_login(self.user2)
        delete_url = reverse('task_delete', args=[self.task3.pk])
        get_response = self.client.get(delete_url)
        self.assertEqual(get_response.status_code, 200)
        post_response = self.client.post(delete_url, follow=True)
        self.assertRedirects(post_response, self.tasks_list)
        self.assertEqual(len(Task.objects.all()), 3)
        content = post_response.content.decode()
        self.assertNotIn('To wash the car', content)
        self.assertContains(post_response, _("Task deleted successfully"))

    def test_delete_task_cant_executor(self):  # if executor != author
        self.client.force_login(self.user3)
        delete_url = reverse('task_delete', args=[self.task2.pk])
        get_response = self.client.get(delete_url, follow=True)
        self.assertRedirects(get_response, self.tasks_list)
        self.assertEqual(len(Task.objects.all()), 4)
        self.assertContains(get_response, 'To grow a flowers')
        self.assertContains(get_response, _("Only its author can delete a task"))

    def test_read_task(self):
        self.client.force_login(self.user1)
        show_task_url = reverse('task_show_index', args=[self.task4.pk])
        get_response = self.client.get(show_task_url)
        content = get_response.content.decode()
        self.assertIn(self.task4.name, content)

    def test_read_tasks_list(self):
        self.client.force_login(self.user2)
        get_response = self.client.get(self.tasks_list)
        content = get_response.content.decode()
        self.assertIn(self.task1.name, content)
        self.assertIn(self.task2.name, content)
        self.assertIn(self.task3.name, content)
        self.assertIn(self.task4.name, content)
    
    def test_task_filter(self):
        self.client.force_login(self.user1)

        request_form_1 = f'{self.tasks_list}?status=3&executor=&label=1'
        get_response = self.client.get(request_form_1)
        filtered_tasks = get_response.context['filter']
        self.assertEqual(len(filtered_tasks.qs), 1)
        result_task1 = filtered_tasks[0]
        self.assertEqual(task.name, 'Make project number 4')
        self.assertEqual(task.status, 'On testing')
        self.assertEqual(task.author, 'Julia21')

        request_form_2 = f'{self.tasks_list}?status=&executor=&label=&only_self_tasks=on'
        get_response = self.client.get(request_form_2)
        filtered_tasks = get_response.context['filter']
        self.assertEqual(len(filtered_tasks.qs), 2)
        result_task1 = filtered_tasks[0]
        self.assertEqual(task.id, 1)
        self.assertEqual(task.status, 'On Testing')
        result_task2 = filtered_tasks[1]
        self.assertEqual(task.id, 2)
        self.assertEqual(task.status, 'New')

        request_form_3 = f'{self.tasks_list}?status=4&executor=2&label='
        get_response = self.client.get(request_form_3)
        filtered_tasks = get_response.context['filter']
        self.assertEqual(len(filtered_tasks.qs), 1)
        result_task1 = filtered_tasks[0]
        self.assertEqual(task.id, 4)
        self.assertEqual(task.status, 'Completed')


class MyTest(TestCase):
    fixtures = ["tasks.json", "statuses.json", "users.json"]

    def test_should_create_task(self):
        task = Task.objects.get(pk=3)
        self.assertEqual(task.name, "To wash the car")
