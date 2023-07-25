from django.urls import reverse
from django.test import Client
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
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # self.assertEqual(User.objects.count(), 2)

    def tset_login_user(self):
        url = reverse('login-api')
        data = {
            'email':'user@example.com',
            'password':'password'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)

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
            "desc": "example",
            "status": "In-progress",
            "priority": "High",
            "completion_date": "2023-09-23",
        }
        response = self.client.post(url, data, format='json')
        print(response.data)
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

# -------------------------------------------------------------------------- !
# negative cases

    def test_signup_existing_email(self):
        url = reverse('register-api')
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        # print(response.status_code)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_invalid_email(self):
        url = reverse('login-api')
        data = {
            'email': 'nonexistent@example.com',  # An email that does not exist in the database
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'error': 'Email incorrect.'})

    def test_login_invalid_password(self):
        url = reverse('login-api')
        data = {
            'email': 'testuser@example.com',
            'password': 'wrongpassword'  # An incorrect password for the user
        }
        response = self.client.post(url, data, format='json')
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'error': 'Invalid password.'})

    def test_todo_list_unauthenticated(self):
        url = reverse('list-todo-api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_create_todo_invalid_data(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('add-todo-api')
        data = {}  # Invalid data
        response = self.client.post(url, data, format='json')
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_update_todo_with_not_found(self):
         self.client.force_authenticate(user=self.user)
         url = 'update-todo-api'
         response = self.client.patch(url)
         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_todo_with_invalid_data(self):
         self.client.force_authenticate(user=self.user)
         url = '/update-todo-api/100/'
         response = self.client.patch(url)

        #  print(response.status_code)
         self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
    
    def test_delete_todo_with_invalid_data(self):
        self.client.force_authenticate(user=self.user)
        url='delete-todo-api'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

# # --------------------------------------------------------------------------- !
# view page

    def test_login(self):
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response, 'todouser/login.html')
        self.assertEqual(response.status_code, 200)
    
    def test_register(self):
        response = self.client.get(reverse('register'))
        self.assertTemplateUsed(response, 'todouser/register.html')
        self.assertEqual(response.status_code, 200)

    def test_profile(self):
        self.client.login(username='testuser', password='testpassword')
        # Test listtodos view for unauthenticated user
        response = self.client.get(reverse('profile'))
        self.assertTemplateUsed(response, 'todouser/profile.html')
        self.assertEqual(response.status_code, 200)

    def test_listtodos_unauthenticated(self):
        self.client.login(username='testuser', password='testpassword')
        # Test listtodos view for unauthenticated user
        response = self.client.get(reverse('todo-list'))
        self.assertTemplateUsed(response, 'todouser/home.html')
        self.assertEqual(response.status_code, 200)

    def test_createtodos_unauthenticated(self):
        self.client.login(username='testuser', password='testpassword')
        # Test createtodos view for unauthenticated user
        response = self.client.post(reverse('todo-create'))
        self.assertTemplateUsed(response, 'todouser/create.html')
        self.assertEqual(response.status_code, 200)

    def test_updatetodos_unauthenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('todo-update', args=[self.todo.id]))
        self.assertTemplateUsed(response, 'todouser/update.html')
        self.assertEqual(response.status_code, 200)
