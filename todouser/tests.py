from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Todo, User
from .factories import TodoFactory

#-------------------------------------------------#
#Positive testcases.
class TodoAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        self.todo = TodoFactory.create(
            user=self.user
        )

    def test_signup(self):
        url = reverse('user_signup')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword'
        }
        response = self.client.post(url, data, format='json')
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_login(self):
        url = reverse('user_login')
        data = {
            'email': 'testuser@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('user_logout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_todo_list(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('api_todo_list')
        response = self.client.get(url)
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['todos']), 1)

    def test_create_todo(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('api_todo_list')
        data = {
            "title": "new",
            "description": "new",
            "status": "new",
            "priority": "new",
            "estimated_date_of_completion": "2023-09-23",
        }
        response = self.client.post(url, data, format='json')
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Todo.objects.count(), 2)

    def test_update_todo(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('api_todo_detail', args=[self.todo.pk])
        data = {
            "title":  'Updated Todo',
            "description": self.todo.description,
            "status": self.todo.status,
            "priority": self.todo.priority,
            "estimated_date_of_completion": self.todo.estimated_date_of_completion,
        }
        response = self.client.patch(url, data, format='json')

        # print(self.todo.title)
        # print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.title, 'Updated Todo')

    def test_delete_todo(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('api_todo_detail', args=[self.todo.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Todo.objects.count(), 0)