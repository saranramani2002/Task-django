from rest_framework import serializers
from .models import Todoapp

class TodoappSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todoapp
        fields = '__all__'
