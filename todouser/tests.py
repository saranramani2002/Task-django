from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Todoapp
from .serilaizers import TodoappSerializer, UserSerializer
from .factories import TodoappFactory, UserFactory

class TodoappTestCase(TestCase):  # users are authenticated
    def setUp(self):
        self.user = User.objects.create_user(   # Create a instance of user
            username='testuser',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')   # user login
        self.todo = TodoappFactory(newuser=self.user)   # Create a todo instance for the logined user

    # view all the todo-list
    def test_todoapp_list_view(self):
        url = reverse('home-todo')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)   # Response is successful
        self.assertContains(response, self.todo.tname)  # Response contains the taskname
        self.assertTemplateUsed(response, 'todouser/home.html')
    
    # views the todo-list based on id
    def test_todoapp_detail_view(self):
        url = reverse('todo-detail', args=[self.todo.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # Response is successful
        self.assertContains(response, self.todo.tname)  # Response contains the taskname
        self.assertTemplateUsed(response, 'todouser/todoapp_detail.html')

    # creates the todo-list
    def test_todoapp_create_view(self):
        url = reverse('todo-create')
        data={                                       # example post datas
            'tname': 'New Task',
            'desc': 'Task Description',
            'status': 'Pending',
            'priority': 'High',
            'completion_date': '2023-07-15',
            'remaining_days': '5 Days',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)   # Response is redirected to the created todo page (by id)
        self.assertEqual(Todoapp.objects.count(), 2)

    # update the existing todo-list
    def test_todoapp_update_view(self):
        url = reverse('todo-update', args=[self.todo.pk])
        data={                                     # example update datas
            'tname': 'Updated Task',
            'desc': 'Updated Description',
            'status': 'Completed',
            'priority': 'Medium',
            'remaining_days':'3 Days' ,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)    # Response is redirected to the updated todo page (by id)
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.tname, 'Updated Task')

    # delete the existing todo-list
    def test_todoapp_delete_view(self):
        url = reverse('todo-delete', args=[self.todo.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)   # Response is redirected to the homepage if deleted, if not deleted redirected to that todo (by id)
        self.assertFalse(Todoapp.objects.filter(pk=self.todo.pk).exists())

#serializers test case               
class TodoSerializerTestCase(TestCase):
    def setUp(self):
        self.tododata = {                     # valid dats for serializers
            'tname': 'React',
            'desc': 'Example task description',
            'status': 'Completed',
            'priority': 'High',
            'completion_date':'2023-07-16',
            'remaining_days': '3 Days',
            'created_at': '2023-07-10',
            'updated_at': '2023-07-10',
        }
          # passs the datas to the serializers

    def test_todo_serializer_valid(self):
        self.serializer = TodoappSerializer(data=self.tododata)
        self.assertTrue(self.serializer.is_valid())         # check and return valid

    def test_todo_serializer_invalid(self):
        invalid_tododata = {                                     # valid datas for serializers
            'tname': '',
            'desc': 'Example task description',
            'status': 'In progress',
            'priority': 'Medium',
            'completion_date':'2023-07-16',
            'remaining_days': '3 Days',
            'created_at': '2023-07-10',
            'updated_at': '2023-07-10',
        }
        serializer = TodoappSerializer(data=invalid_tododata)      # passs the datas to the serializers
        self.assertFalse(serializer.is_valid())                    # check and return valid if datas are invalid

class UserSerializerTestCase(TestCase):
    def setUp(self):
        self.userdata = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'testpassword',
        }
        self.serializer = UserSerializer(data=self.userdata)

    def test_user_serializer_valid(self):
        self.assertTrue(self.serializer.is_valid())

    def test_user_serializer_invalid(self):
        invalid_userdata = {
            'email': 'email.gmail.com',
            'username': 'testuser',
            'password': 'testpassword',
        }
        serializer = UserSerializer(data=invalid_userdata)
        self.assertFalse(serializer.is_valid())

    def test_create_user(self):
        self.assertTrue(self.serializer.is_valid())  # Call is_valid() before accessing validated_data
        user = self.serializer.create(self.serializer.validated_data)
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, self.userdata['email'])
        self.assertEqual(user.username, self.userdata['username'])
