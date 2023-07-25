from rest_framework import generics, permissions
from .serializers import TodoSerializer, TodoCompleteSerializer
from todo.models import Todo
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth import login
from rest_framework.authtoken.models import Token


@csrf_exempt
def signup(request):
    if request.method == "POST":
        try:
            data = JSONParser().parse(request)
            user = User.objects.create_user(
                data["username"], password=request.data["password"]
            )
            user.save()
            token = Token.objects.create(user=user)
            return JsonResponse({"token": str(token)}, status=201)
        except IntegrityError:
            return JsonResponse(
                {"error": "Username already taken. Please choose new  Username"},
                status=400,
            )


@csrf_exempt
def login(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        user = User.objects.create_user(
            data["username"], password=request.data["password"]
        )

        if user is None:
            return JsonResponse(
                {"error": "Could not login.Check username and password"}, status=400
            )
        else:
            try:
                token = Token.objects.get(user=user)
            except:
                token = Token.objects.create(user=user)

            return JsonResponse({"token": str(token)}, status=200)


class TodoCompletedList(generics.ListAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user, date_completed__isnull=False).order_by(
            "-date_completed"
        )


class TodoCreateList(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user, date_completed__isnull=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TodoEditList(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user)


class TodoCompleteList(generics.UpdateAPIView):
    serializer_class = TodoCompleteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user)

    def perform_update(self, serializer):
        serializer.instance.date_completed = timezone.now()
        serializer.save()
