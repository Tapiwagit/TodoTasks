from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.signup),
    path("todos/", views.TodoCreateList.as_view()),
    path("todos/<int:pk>", views.TodoEditList.as_view()),
    path("todos/<int:pk>/complete", views.TodoCompleteList.as_view()),
    path("todos/completed/", views.TodoCompletedList.as_view()),
    path("login/", views.login),
]
