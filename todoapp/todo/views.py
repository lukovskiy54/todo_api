from django.shortcuts import render
from rest_framework import viewsets
from .models import TodoItem
from .serializers import TodoItemSerizlizer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import GoogleTokenSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
import requests

class ToDoViewset(viewsets.ModelViewSet):
    queryset = TodoItem.objects.all()
    serializer_class = TodoItemSerizlizer
    
    def get_queryset(self):
        email = self.request.query_params.get('email')
        print(f'email {email}')
        if email:
                return TodoItem.objects.filter(user_email=email)
        return TodoItem.objects.none()
    
    def perform_create(self, serializer):
        user_email = serializer.validated_data.get('user_email', None)
        serializer.save(user_email=user_email)
        print("user_email",user_email)
        if user_email:
            user = get_object_or_404(User, email=user_email)
            serializer.save(user=user)
            print("Serialized Data:", serializer.data)
        else:
            # Handle the case where user email is not provided
            response = {'message': 'User email is required'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        
User = get_user_model()

class GoogleLoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = GoogleTokenSerializer(data=request.data)
        
        if serializer.is_valid():
            access_token = serializer.validated_data.get('access_token')
            
   
            google_response = requests.get(
                f'https://www.googleapis.com/oauth2/v3/tokeninfo?access_token={access_token}'
            )
            
            if google_response.status_code == 200:
                google_data = google_response.json()
                
                # Get user info
                email = google_data.get('email')
                first_name = google_data.get('given_name', '')
                last_name = google_data.get('family_name', '')
                
                # Find or create user
                user, created = User.objects.get_or_create(email=email, defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'username': email,  # Assuming username is based on email
                })
                
                # Generate JWT token
                refresh = RefreshToken.for_user(user)
                data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid Google token'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)