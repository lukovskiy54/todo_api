"""
URL configuration for todoapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

from todo.views import ToDoViewset,GoogleLoginView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('', ToDoViewset, basename='todos')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)), 
    path('auth/', include('dj_rest_auth.urls')),
    path('accounts/', include('allauth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('socialaccounts/', include('allauth.socialaccount.urls')),
    path('auth/google/', include('allauth.socialaccount.providers.google.urls')),
    path('google-login/', GoogleLoginView.as_view(), name='google-login'),
]