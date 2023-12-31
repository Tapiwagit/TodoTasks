from rest_framework import serializers
from todo.models import Todo


class TodoSerializer(serializers.ModelSerializer):
    created = serializers.ReadOnlyField()
    date_completed = serializers.ReadOnlyField()

    class Meta:
        model = Todo
        fields = ["id", "title", "memo", "date_completed", "created", "important"]


class TodoCompleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ["id"]
        read_only_fields = ["title", "memo", "date_completed", "created", "important"]
