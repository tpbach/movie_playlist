# from django.contrib.auth.models import Permission
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from . models import User
from . serializers import RegisterSerializer
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout


class RegisterUser(APIView):
    #Register a new users
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=201)

        if User.objects.filter(username=request.data['username']).exists():
            return Response({"Status 0": "User with this username already exist"}, status=status.HTTP_409_CONFLICT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginUser(APIView):
    #allows users created to login.
    def post(self, request):
        user = authenticate(request, username=request.data['username'], password=request.data['password'])
        if user is not None:
            login(request, user)
            return HttpResponse("Login sucessful", status=status.HTTP_201_CREATED)
        else:
            return HttpResponse("Login Failed.", status=status.HTTP_400_BAD_REQUEST)

class LogoutUser(APIView):
    def post(self, request):
        logout(request)
        return HttpResponse("Logout successful", status=201)