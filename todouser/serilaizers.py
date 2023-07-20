from rest_framework import serializers
from .models import Todoapp
from django.contrib.auth.models import User


class TodoappSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Todoapp
        fields = ['id','tname','desc','status','priority','completion_date','created_at','updated_at',]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
