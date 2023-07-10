import factory
from django.contrib.auth.models import User
from todouser.models import Todoapp
from django.urls import reverse
from django.contrib.auth.decorators import login_required


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', 'testpassword')    

class TodoappFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Todoapp

    tname = factory.Sequence(lambda n: f'Task {n}')
    desc = 'Task Description'
    status = 'Pending'
    priority = 'High'
    completion_date = '2023-07-10'
    remaining_days = 7
    newuser = factory.SubFactory(UserFactory)

class ProfileFactory(factory.django.DjangoModelFactory):
    model = User
    
    username = factory.Faker('name')