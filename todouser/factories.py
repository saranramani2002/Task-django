import factory
from django.contrib.auth.models import User
from todouser.models import Todoapp
from faker import Faker
fake = Faker()

# class UserFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = User

#     username = factory.sequence(lambda n: f"user{n}")
#     password = factory.PostGenerationMethodCall('set_password', 'password')
#     email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")    

class TodoappFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Todoapp

    # newuser = factory.SubFactory(UserFactory)
    tname = fake.word()
    desc = fake.sentence(nb_words=5)
    status = fake.random_element(elements=('Pending', 'In Progress', 'Completed'))
    priority = fake.random_element(elements=('Low', 'Medium', 'High'))
    completion_date = fake.future_date(end_date='+30d')

class ProfileFactory(factory.django.DjangoModelFactory):
    model = User
    
    username = factory.Faker('name')
