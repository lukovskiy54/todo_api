from rest_framework import serializers

from .models import TodoItem

class TodoItemSerizlizer(serializers.ModelSerializer):
    class Meta:
        model = TodoItem
        fields = ['title','user_email','completed','id']
        
        
        
class GoogleTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField()