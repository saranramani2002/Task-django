from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from . import views1
from . import api

urlpatterns = [
    # old paths
    # path('register/', views.register, name='register'),
    # path('', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    # path('profile/', views.profile, name='profile'),

    # template path
    # path('registertodo/', views1.registerform, name='register'),
    # path('logintodo/', views1.loginform, name='login'),
    # path('logouttodo/', views1.logoutform, name='logout'),
    # path('profiletodo/', views1.progilrform, name='profile'),

    # api path
    # path('loginapi/', api.LoginViewApi.as_view(), name='loginapi'),
    # path('logoutapi/', api.LogoutViewApi.as_view(), name='logoutapi'),
    # path('registerapi/', api.SignInViewApi.as_view(), name='registerapi'),
]
