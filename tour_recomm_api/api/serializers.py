from rest_framework import serializers
from .models import User



class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id', 'email', 'fullname', 'dob', 'gender', 'role', 'created_at')
    

class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'pw', 'fullname', 'role')

    email = serializers.EmailField()
    pw = serializers.CharField(max_length = 30)
    fullname = serializers.CharField(max_length = 50)
    role = serializers.CharField()
    