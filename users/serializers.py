from rest_framework import serializers
from .models import User

class StudentRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email', 'phonenumber']

class StudentLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

class StudentViewSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'phonenumber']