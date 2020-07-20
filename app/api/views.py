from django.utils.decorators import method_decorator
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from drf_yasg.utils import swagger_auto_schema

from .models import Todo
from .serializers import UserSignupSerializer, UserLoginSerializer, \
                         TodoSerializer


class UserSignupView(generics.CreateAPIView):
    '''
    User Signup

    Endpoint for registration new user
    '''
    serializer_class = UserSignupSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {'message': 'User signup successfully',
                    'result': 'New user created: ' + request.data['email']}
        return Response(response, status=status.HTTP_201_CREATED)


class UserLoginView(generics.CreateAPIView):
    '''
    User Login

    Endpoint for JWT Authorization
    '''
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {'message': 'User logged in successfully',
                    'result': 'User logged in: ' + request.data['email'],
                    'token': serializer.data['token']}
        return Response(response, status=status.HTTP_200_OK)


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description="Endpoint for viewing todo list",
    operation_summary='ToDo List',
))
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_description="Endpoint for creation a new task",
    operation_summary='Create New Task',
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_description="Endpoint for reading a task",
    operation_summary='Read Task',
))
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_description="Endpoint for updating a task",
    operation_summary='Update Task',
))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    operation_description="Endpoint for partial updating a task",
    operation_summary='Partial Update Task',
))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_description="Endpoint to delete a task",
    operation_summary='Delete Task',
))
class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = (IsAuthenticated, )
    authentication_class = JSONWebTokenAuthentication
