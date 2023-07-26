from rest_framework import serializers
from .models import Todoapp
from django.contrib.auth.models import User


class TodoappSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Todoapp
        fields = ['id','tname','desc','status','priority','completion_date','created_at','updated_at','user','days_remaining']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("Email is required.")
        existing_users = User.objects.filter(email=value)
        if existing_users.exists():
            raise serializers.ValidationError("Email already exists.")
        return value