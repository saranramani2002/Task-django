from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from . import views1
from . import apis


urlpatterns = [
    # render templates
    path('hometodo/', views1.listtodos, name="todo-list"),
    path('addtodo/', views1.createtodos, name="todo-create"),
    path('updatetodo/<int:pk>/', views1.updatetodos, name="todo-update"),
    path('registertodo/', views1.registerform, name='register'),
    path('', views1.loginform, name='login'),
    path('logouttodo/', views1.logoutform, name='logout'),
    path('profiletodo/', views1.progilrform, name='profile'),


    # api
    path('listapi/', apis.TodoList.as_view(), name="list-todo-api"),
    path('addapi/', apis.TodoCreate.as_view(), name="add-todo-api"),
    path('updateapi/', apis.TodoUpdate.as_view(), name="update-todo-api"),
    path('deleteapi/<int:pk>/', apis.TodoDelete.as_view(), name="delete-todo-api"),
    path('loginapi/', apis.LoginViewApi.as_view(), name='loginapi'),
    path('logoutapi/', apis.LogoutViewApi.as_view(), name='logoutapi'),
    path('registerapi/', apis.SignInViewApi.as_view(), name='registerapi'),
]