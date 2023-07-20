from .models import Todoapp
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .serilaizers import TodoappSerializer, UserSerializer
from rest_framework.decorators import APIView, permission_classes



class TodoList(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            todo = Todoapp.objects.all()
            serializer = TodoappSerializer(todo, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            pass

class TodoCreate(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            # user = request.data
            # request.data['user'] = user.id 
            serializer = TodoappSerializer(data=request.data) 
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
           print(e)
           pass

class TodoUpdate(APIView):
    # permission_classes = [IsAuthenticated]
    def patch(self, request, pk):
        try:
            todo = Todoapp.objects.get(id=pk)
            serializer = TodoappSerializer(todo, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Todoapp.DoesNotExist:
            return Response({"Detail":"Nothing In This Id, Can't Update"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            pass

class TodoDelete(APIView):
    # permission_classes = [IsAuthenticated]
    def delete(self, request, pk):
        try:
            todo = Todoapp.objects.get(id=pk)
            todo.delete()
            return Response({"Detail":"Successfully Deleted"},status=status.HTTP_204_NO_CONTENT)
        except Todoapp.DoesNotExist:
            return Response({"Detail":"Nothing In This Id, Can't Delete!"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            pass

# apis for user -----------------------------------------------------
class LoginViewApi(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, username=username, email=email, password=password)
        if user is not None:
            token = Token.objects.get(user=user)
            res = {
                "token":token.key,
                "Details":"User was authenticated and Login successfully!"
            }
            return Response(res,status=200)
        else: 
            return Response({"Details":"Login Failed"},status=400)

class SignInViewApi(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects. create(user=user)
            res = {
                "token":token.key,
                "user":serializer.data
            }
            return Response(res,status=201)
        return Response(serializer.errors,status=400)

class LogoutViewApi(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        request.user.auth_token.delete()
        return Response(status=200)