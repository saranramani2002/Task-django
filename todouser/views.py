from django.shortcuts import render, redirect
from .models import Todoapp
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


@login_required
def listtodos(request):
    user = request.user
    return render(request, 'todouser/home.html', {'username':user})

@login_required
def createtodos(request):
    # if request.method == 'POST':
    #     form_data = request.POST
    #     user = request.user
    #     todo_data = {
    #         'tname': form_data['task-name'],
    #         'desc': form_data['task-desc'],
    #         'status': form_data['task-status'],
    #         'priority': form_data['task-priority'],
    #         'completion_date': form_data['task-cmplt-date'],
    #         'user_id': user,
    #     }
    #     Todoapp.objects.create(**todo_data)
    #     return redirect('todo-list')
    return render(request, 'todouser/create.html')

@login_required
def updatetodos(request, pk):
    try:
        todoData = Todoapp.objects.get(id=pk)
    except Todoapp.DoesNotExist:
        todoData = None
    
    return render(request, 'todouser/update.html', {'todos' : todoData})


def loginform(request):   
    return render(request, 'todouser/login.html')


def registerform(request):
    return render(request, 'todouser/register.html')

@login_required
def progilrform(request):
    return render(request, 'todouser/profile.html')

def check_duplicate_title(request):
    title = request.GET.get('tname', None)
    if title:
        if Todoapp.objects.filter(tname=title).exists():
            return JsonResponse({'exists': True})
    return JsonResponse({'exists': False})