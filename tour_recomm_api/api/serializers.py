from rest_framework import serializers
from .models import *


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id', 'email', 'fullname', 'dob', 'gender', 'role', 'created_at')
    
class UserLoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'pw')
    
    email = serializers.EmailField()
    pw = serializers.CharField(max_length = 30)

class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'pw', 'fullname')

    email = serializers.EmailField()
    pw = serializers.CharField(max_length = 30)
    fullname = serializers.CharField(max_length = 50)

# ====================================================
# Tourist Serializer
class TouristSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tourist
        fields = '__all__'

# ====================================================
# History Serializer
class HistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = History
        fields = '__all__'
    #     extra_fields = ['tourist']
    
    # tourist = serializers.SerializerMethodField()

    # def get_tourist(self, obj):
    #     return TouristSerializer(obj).data