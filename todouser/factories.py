# import factory
# from django.contrib.auth.models import User
# from .models import Todoapp

# class UserFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = User

#     username = factory.Sequence(lambda n: f'user{n}')
#     password = 'password123'

# class TodoappFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Todoapp

#     tname = factory.Sequence(lambda n: f'Task {n}')
#     desc = 'Task Description'
#     status = 'Pending'
#     priority = 'High'
#     completion_date = '2023-07-10'
#     remaining_days = 7
#     newuser = factory.SubFactory(UserFactory)
