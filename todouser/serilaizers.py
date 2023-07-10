from rest_framework import serializers
from .models import Todoapp
from django.contrib.auth.models import User

class TodoappSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todoapp
        fields = ['tname','desc','status','priority','completion_date','remaining_days','created_at','updated_at']

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user