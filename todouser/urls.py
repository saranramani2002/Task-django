from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from . import apis


urlpatterns = [
    # render templates
    path('hometodo/', views.listtodos, name="todo-list"),
    path('addtodo/', views.createtodos, name="todo-create"),
    path('updatetodo/<int:pk>/', views.updatetodos, name="todo-update"),

    path('duplicate_taskname/',views.check_duplicate_title, name='check-duplicate'),

    path('registertodo/', views.registerform, name='register'),
    path('', views.loginform, name='login'),
    path('profiletodo/', views.progilrform, name='profile'),


    # api
    path('listapi/', apis.TodoList.as_view(), name="list-todo-api"),
    path('addapi/', apis.TodoCreate.as_view(), name="add-todo-api"),
    path('updateapi/<int:pk>/', apis.TodoUpdate.as_view(), name="update-todo-api"),
    path('deleteapi/<int:pk>/', apis.TodoDelete.as_view(), name="delete-todo-api"),
    
    path('loginapi/', apis.LoginViewApi.as_view(), name='loginapi'),
    path('logoutapi/', apis.LogoutViewApi.as_view(), name='logoutapi'),
    path('registerapi/', apis.SignInViewApi.as_view(), name='registerapi'),
]