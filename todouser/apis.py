from .models import Todoapp, User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated
from .serilaizers import TodoappSerializer, UserSerializer
from django.core.exceptions import ObjectDoesNotExist


# apis for Users -----------------------------------------------------

class SignInViewApi(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)


class LoginViewApi(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return Response({'message': 'Login successful.'}, status=status.HTTP_200_OK)
        else: 
            if not User.objects.filter(email=email).exists():
                    return Response({'error': 'Email incorrect.'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'error': 'Invalid password.'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutViewApi(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        username = request.user.username
        logout(request)
        return Response({"message": f"Successfully loged out {username}!"}, status=status.HTTP_200_OK)


# api's for CRUD Operations --------------------------------------------------------------------------

class TodoList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        todo = Todoapp.objects.filter(user=user)
        serializer = TodoappSerializer(todo, many=True)
        return Response({'todos':serializer.data}, status=status.HTTP_200_OK)

class TodoCreate(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,req):
        data = req.data.copy()
        user = req.user
        data['user'] = user.id
        # print(user.id)
        serializer=TodoappSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)


class TodoUpdate(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self, request, pk):
        try:
            todo = Todoapp.objects.get(id=pk)
            serializer = TodoappSerializer(todo, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({"Error":"Task not found!"}, status=status.HTTP_404_NOT_FOUND)

class TodoDelete(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, pk):
        try:
            todo = Todoapp.objects.get(id=pk)
            todo.delete()
            return Response({"Detail":"Successfully Deleted"},status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response({"Error":"Task not found!"}, status=status.HTTP_404_NOT_FOUND)