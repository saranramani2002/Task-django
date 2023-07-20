from django.shortcuts import render
from .models import Todoapp
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response


# @login_required
def listtodos(request):
    return render(request, 'todouser/home.html')

# @login_required
def createtodos(request):   
    return render(request, 'todouser/todo_create.html')

# @login_required
def updatetodos(request, pk):
    try:
        todoData = Todoapp.objects.get(id=pk)
    except Todoapp.DoesNotExist:
        return Response ({"Detail":"Nothing In This Id"})
    
    return render(request, 'todouser/todo_update.html', {'todos' : todoData})

# @login_required
def loginform(request):   
    return render(request, 'users/login.html')

# @login_required
def registerform(request):
    return render(request, 'users/register.html')

# @login_required
def logoutform(request):
    return render(request, 'users/logout.html')

@login_required
def progilrform(request):
    return render(request, 'users/profile.html')

