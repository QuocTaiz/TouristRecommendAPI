from ..services import HashPw, TokenManager
from django.shortcuts import render
from datetime import datetime
from django.utils import timezone
from django.contrib.auth import authenticate
from ..models import User, CustomResponse, Token
from ..serializers import *
from rest_framework.views import APIView
from rest_framework import status
# Create your views here.

class UserDetail(APIView):
    
    http_method_names = ['get', 'head', 'post']

    def get(self, request):
        
        role_accept = ['admin']

        token = request.headers.get('token')
        if not TokenManager.verify(token) in role_accept:
            return CustomResponse(status.HTTP_401_UNAUTHORIZED, 'UNAUTHORIZED!')

        list_user = User.objects.all()
        data_serializer = UserSerializer(list_user, many=True)
        return CustomResponse(status.HTTP_200_OK, 'Get all user successful!', data_serializer.data)
    
    def post(self, request):
        
        default_role = 'user'

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
            dt_created = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
            user = User.objects.create(email=email, hashpw=hashpw, fullname=fullname, role=default_role, created_at=dt_created)
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

        token = request.headers.get('token')

        if not TokenManager.verify(token):
            return CustomResponse(status.HTTP_401_UNAUTHORIZED, 'UNAUTHORIZED!')

        try:
            obj = User.objects.get(id=id)

        except User.DoesNotExist:
            return CustomResponse(status= status.HTTP_404_NOT_FOUND, message= 'Not found this id!')
        
        serializer = UserSerializer(obj, data= request.data, partial= True)

        if serializer.is_valid():
            serializer.save()
            return CustomResponse(status= status.HTTP_205_RESET_CONTENT, message= 'Update successful! Please reset UI')
        return CustomResponse(status= status.HTTP_400_BAD_REQUEST, message= 'Data not vaild!')

    def delete(self, request, id):

        role_accept = ['admin']

        token = request.headers.get('token')

        if not TokenManager.verify(token) in role_accept:
            return CustomResponse(status.HTTP_401_UNAUTHORIZED, 'UNAUTHORIZED!')

        try: 
            obj = User.objects.get(id=id)

        except User.DoesNotExist:
            return CustomResponse(status.HTTP_404_NOT_FOUND, 'User not found!')
        
        obj.delete()
        TokenManager.delete(Token.objects.get(key = token))
        return CustomResponse(status.HTTP_204_NO_CONTENT, 'Delete user successful!')
    
class UserLogin(APIView):
    http_method_names = ['post']

    def post(self, request):

        serializer = UserLoginSerializer(data = request.data)

        if not serializer.is_valid():
            return CustomResponse(status.HTTP_400_BAD_REQUEST, 'Data not valid!')

        email = request.data['email']
        hashpw = HashPw.hash(request.data['pw'])

        try: 
            user = User.objects.get(email = email, hashpw = hashpw)
        except User.DoesNotExist:
            return CustomResponse(status.HTTP_404_NOT_FOUND, 'User not found! Login failed!')
        
        try:
            token = Token.objects.get(user_id = user.id)
        except Token.DoesNotExist:
            user_id = user.id
            token = TokenManager.create(user_id)
            return CustomResponse(status.HTTP_200_OK, 'Login successful!', token.key)
        
        token = TokenManager.update(token)

        return CustomResponse(status.HTTP_200_OK, 'Login successful!', token.key)





    