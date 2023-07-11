from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse
from .factories import UserFactory, ProfileFactory, TodoappFactory

class RegisterTestCase(APITestCase):
    def test_register_view(self):
        data = {
            "username":"testuser",
            "email":"test@gmail.com",
            "password1":"testpassword",
            "password2":"testpassword"
        }
        # user = UserFactory(**data)
        url = ('/register/')
        response = self.client.post(url,data)
        print(response)
        self.assertEqual(response.status_code, 302)
    
    def test_invalid_register_view(self):
        data = {
            "username":"",
            "email":"test@gmail.com",
            "password1":"testpassword",
            "password2":"testpassword"
        }
        # user = UserFactory(**data)
        url = ('/register/')
        response = self.client.post(url,data)
        print(response)
        self.assertNotEqual(response.status_code, 302)
    
    def test_get_register_view(self):
        data = {
            "username":"testuser",
            "email":"test@gmail.com",
            "password1":"testpassword",
            "password2":"testpassword"
        }
        url = ('/register/')
        response = self.client.get(url,data)
        # print(response)
        self.assertEqual(response.status_code, 200)


class ProfileTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()
        # self.user = User.objects.create_user(   # Create a instance of user
        #     username='testuser',
        #     password='testpassword'
        # )
        # self.client.login(username='testuser', password='testpassword')   # user login
        # self.todo = TodoappFactory(newuser=self.user)   # Create a todo instance for the logined user
    
    def test_profile_view(self):
        self.client.force_login(self.user)
        url = reverse('profile')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
    
    def test_profile_view_unauthenticated(self):
        url = reverse('profile')
        response = self.client.get(url)
        print(response)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/?next=/profile/')