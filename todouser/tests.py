from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Todoapp
from .factories import UserFactory, TodoappFactory

class TodoappTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')
        self.todo = TodoappFactory(newuser=self.user)

    def test_todoapp_list_view(self):
        response = self.client.get(reverse('home-todo'))
        print(response)
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, self.todo.tname)

    def test_todoapp_detail_view(self):
        response = self.client.get(reverse('todo-detail', args=[self.todo.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.todo.tname)

    def test_todoapp_create_view(self):
        response = self.client.post(reverse('todo-create'), data={
            'tname': 'New Task',
            'desc': 'Task Description',
            'status': 'Pending',
            'priority': 'High',
            'completion_date': '2023-07-15',
            'remaining_days': 5,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Todoapp.objects.count(), 2)

    def test_todoapp_update_view(self):
        response = self.client.post(reverse('todo-update', args=[self.todo.pk]), data={
            'tname': 'Updated Task',
            'desc': 'Updated Description',
            'status': 'Completed',
            'priority': 'Medium',
            'remaining_days': 3,
        })
        self.assertEqual(response.status_code, 302)
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.tname, 'Updated Task')

    def test_todoapp_delete_view(self):
        response = self.client.post(reverse('todo-delete', args=[self.todo.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Todoapp.objects.filter(pk=self.todo.pk).exists())
