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

# -------------------------------------------------------------------------- !
# negative cases

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
    
    def test_update_todo_with_invalid_data(self):
         self.client.force_authenticate(user=self.user)
         url = 'update-todo-api'
         response = self.client.patch(url)
         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_todo_with_invalid_data(self):
        self.client.force_authenticate(user=self.user)
        url='delete-todo-api'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

# --------------------------------------------------------------------------- !
# view page

class TodoAppViewsTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a test Todo item
        self.todo = Todoapp.objects.create(tname='Test Todo', user=self.user)

        # Initialize the test client
        self.client = Client()

    def test_listtodos_authenticated(self):
        # Test listtodos view for authenticated user
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('todo-list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todouser/home.html')
        # self.assertContains(response, 'testuser')  # Ensure the username is present in the response

    def test_listtodos_unauthenticated(self):
        # Test listtodos view for unauthenticated user
        response = self.client.get(reverse('todo-list'))

        # It should redirect to the login page for unauthenticated users
        self.assertRedirects(response, '/?next=/hometodo/', fetch_redirect_response=False)

    def test_createtodos_authenticated(self):
        # Test createtodos view for authenticated user
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('todo-create'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todouser/create.html')

    def test_createtodos_unauthenticated(self):
        # Test createtodos view for unauthenticated user
        response = self.client.get(reverse('todo-create'))

        # It should redirect to the login page for unauthenticated users
        self.assertRedirects(response, '/?next=/addtodo/', fetch_redirect_response=False)

    def test_updatetodos_authenticated(self):
        # Test updatetodos view for authenticated user with a valid Todo item id (pk)
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('todo-update', args=[self.todo.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todouser/update.html')

    def test_updatetodos_unauthenticated(self):
        # Test updatetodos view for unauthenticated user with a valid Todo item id (pk)
        response = self.client.get(reverse('todo-update', args=[self.todo.id]))

        # It should redirect to the login page for unauthenticated users
        self.assertRedirects(response, f'/?next=/updatetodo/{self.todo.id}/', fetch_redirect_response=False)

    # def test_updatetodos_invalid_pk(self):
    #     # Test updatetodos view with an invalid Todo item id (pk)
    #     self.client.login(username='testuser', password='testpassword')
    #     invalid_pk = self.todo.id + 1  # Assuming this pk does not exist
    #     response = self.client.get(reverse('todo-update', args=[invalid_pk]))
    #     print(response.status_code)

    #     self.assertEqual(response.status_code, 404)

    # Add more test cases for other views if needed
