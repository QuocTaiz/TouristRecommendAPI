import json
from django.shortcuts import render
from datetime import datetime
from .models import User, CustomResponse
from .serializers import UserSerializer, UserCreateSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
# Create your views here.

class UserView(APIView):
    
    permission_classes = (permissions.AllowAny,)
    http_method_names = ['get', 'head', 'post', 'patch']

    def get(self, request):
        list_user = User.objects.all()
        data_serializer = UserSerializer(list_user, many=True)
        return CustomResponse(status = status.HTTP_200_OK, message = 'ok', data = data_serializer.data)
    
    def post(self, request):
        user_data = UserCreateSerializer(data=request.data)
        if not user_data.is_valid():
            return CustomResponse(status = status.HTTP_400_BAD_REQUEST, message = 'Data not valid')
        email = user_data.data['email']
        pw = user_data.data['pw']
        hashpw = pw                           # hash pw here                  
        fullname = user_data.data['fullname']
        role = user_data.data['role']
        dt_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user = User.objects.create(email=email, hashpw=hashpw, fullname=fullname, role=role, created_at=dt_created)
        return CustomResponse(status = status.HTTP_200_OK, message='Create user successful!', data=user.id)
    
