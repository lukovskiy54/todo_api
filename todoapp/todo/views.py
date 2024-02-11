from django.shortcuts import render
from rest_framework import viewsets
from .models import TodoItem
from .serializers import TodoItemSerizlizer


class ToDoViewset(viewsets.ModelViewSet):
    queryset = TodoItem.objects.all()
    serializer_class = TodoItemSerizlizer
