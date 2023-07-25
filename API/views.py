from django.shortcuts import render, redirect
from rest_framework import generics, permissions
from .serializers import TodoSerializer, TodoCompleteSerializer
from todo.models import Todo
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import JsonResponse


@csrf_exempt
def signup(request):
    if request.method == "POST":
        try:
            data = JSONParser().parse(request)
            user = User.objects.create_user(
                data["username"], password=request.data["password"]
            )
            user.save()
            login(request, user)
            return JsonResponse({"token": ""}, status=201)
        except IntegrityError:
            return JsonResponse(
                {"error": "username already taken. Please choose new  username"}
            )


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
