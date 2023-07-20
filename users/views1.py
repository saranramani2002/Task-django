from django.shortcuts import render


def loginform(request):   
    return render(request, 'users/login.html')

def registerform(request):
    return render(request, 'users/register.html')

def logoutform(request):
    return render(request, 'users/logout.html')

def progilrform(request):
    return render(request, 'users/profile.html')