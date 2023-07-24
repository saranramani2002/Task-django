from django.shortcuts import render
from .models import Todoapp
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


# @login_required
def listtodos(request):
    user = request.user
    return render(request, 'todouser/home.html', {'username':user})

# @login_required
def createtodos(request):   
    return render(request, 'todouser/create.html')

# @login_required
def updatetodos(request, pk):
    try:
        todoData = Todoapp.objects.get(id=pk)
    except Todoapp.DoesNotExist:
        todoData = None
    
    return render(request, 'todouser/update.html', {'todos' : todoData})

# @login_required
def loginform(request):   
    return render(request, 'todouser/login.html')

# @login_required
def registerform(request):
    return render(request, 'todouser/register.html')

# @login_required
def progilrform(request):
    return render(request, 'todouser/profile.html')

def check_duplicate_title(request):
    title = request.GET.get('tname', None)
    if title:
        if Todoapp.objects.filter(tname=title).exists():
            return JsonResponse({'exists': True})
    return JsonResponse({'exists': False})