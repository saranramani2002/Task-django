from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Todoapp, User
from .factories import TodoappFactory

#-------------------------------------------------#

class TodoAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        self.todo = TodoappFactory.create(
            user=self.user
        )

    def test_signup(self):
        url = reverse('register-api')
        data = {
            'username': 'user',
            'email': 'user@example.com',
            'password': 'password'
        }
        response = self.client.post(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_login(self):
        url = reverse('login-api')
        data = {
            'email': 'testuser@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('logout-api')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_todo_list(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('list-todo-api')
        response = self.client.get(url)
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['todos']), 1)

    def test_create_todo(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('add-todo-api')
        data = {
            "tname": "new task",
            "desc": "new description",
            "status": "In-progress",
            "priority": "High",
            "completion_date": "2023-09-23",
        }
        response = self.client.post(url, data, format='json')
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Todoapp.objects.count(), 2)

    def test_update_todo(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('update-todo-api', args=[self.todo.pk])
        data = {
            "tname":  'Updated Todo',
            "desc": self.todo.desc,
            "status": self.todo.status,
            "priority": self.todo.priority,
            "completion_date": self.todo.completion_date,
        }
        response = self.client.patch(url, data, format='json')

        # print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.tname, 'Updated Todo')

    def test_delete_todo(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('delete-todo-api', args=[self.todo.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Todoapp.objects.count(), 0)