import json
from .services import HashPw
from django.shortcuts import render
from datetime import datetime
from .models import User, CustomResponse
from .serializers import UserSerializer, UserCreateSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
# Create your views here.

class UserDetail(APIView):
    
    http_method_names = ['get', 'head', 'post']

    def get(self, request):

        list_user = User.objects.all()
        data_serializer = UserSerializer(list_user, many=True)
        return CustomResponse(status.HTTP_200_OK, 'Get all user successful!', data_serializer.data)
    
    def post(self, request):

        data_serializer = UserCreateSerializer(data=request.data)
        if not data_serializer.is_valid():
            return CustomResponse(status.HTTP_400_BAD_REQUEST, 'Data not valid!')
        email = data_serializer.data['email']

        try:
            obj = User.objects.get(email=email)
            return CustomResponse(status.HTTP_400_BAD_REQUEST, 'This email has been registered!')
        except User.DoesNotExist:
            pw = data_serializer.data['pw']
            hashpw = HashPw.hash(pw)                                   
            fullname = data_serializer.data['fullname']
            role = data_serializer.data['role']
            dt_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            user = User.objects.create(email=email, hashpw=hashpw, fullname=fullname, role=role, created_at=dt_created)
            return CustomResponse(status.HTTP_201_CREATED, 'Create user successful!', data=user.id)

class UserInfo(APIView):

    http_method_names = ['get', 'head', 'patch', 'delete']

    def get(self, request, id):
        try:
            obj = User.objects.get(id=id)

        except User.DoesNotExist:
            return CustomResponse(status.HTTP_404_NOT_FOUND, 'User not found!')
        
        serializer = UserSerializer(obj)
        return CustomResponse(status.HTTP_200_OK, 'Get user successful!', serializer.data)
        

    def patch(self, request, id):

        try:
            obj = User.objects.get(id=id)

        except User.DoesNotExist:
            return CustomResponse(status= status.HTTP_404_NOT_FOUND, message= 'Not found this id!')
        
        serializer = UserSerializer(obj, data= request.data, partial= True)

        if serializer.is_valid():
            serializer.save()
            return CustomResponse(status= status.HTTP_205_RESET_CONTENT, message= 'Update successful! Please reset UI')
        return CustomResponse(status= status.HTTP_400_BAD_REQUEST, message= 'Data not vaild!')
