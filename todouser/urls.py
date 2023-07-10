from django.urls import path
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('home/', views.TodoappListView.as_view(), name='home-todo'),
    path('todo/<int:pk>/', views.TodoappDetailView.as_view(), name='todo-detail'),
    path('todo/new/', views.TodoappCreateView.as_view(), name='todo-create'),
    path('todo/<int:pk>/update/', views.TodoappUpdateView.as_view(), name='todo-update'),
    path('todo/<int:pk>/delete/', views.TodoappDeleteView.as_view(), name='todo-delete'),
]
    