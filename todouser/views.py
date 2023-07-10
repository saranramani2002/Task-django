from django.db import models
from django.shortcuts import render
from .models import Todoapp
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin


class TodoappListView(generic.ListView):
    model = Todoapp
    template_name = 'todouser/home.html'
    context_object_name = 'todolist'
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Todoapp.objects.filter(newuser=self.request.user)

class TodoappDetailView(generic.DetailView):
    model = Todoapp

class TodoappCreateView(LoginRequiredMixin, generic.CreateView):
    model = Todoapp
    fields = ['tname','desc','status','priority','completion_date','remaining_days']
    
    def form_valid(self, form):
        form.instance.newuser = self.request.user
        return super().form_valid(form)

class TodoappUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Todoapp
    fields = ['tname','desc','status','priority','completion_date','remaining_days']
    
    def form_valid(self, form):
        form.instance.newuser = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.get_object():
            return True
        return False

class TodoappDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Todoapp
    success_url = '/home/'
    
    def test_func(self):
        post = self.get_object()
        if self.get_object():
            return True
        return False