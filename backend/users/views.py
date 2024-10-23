from django.shortcuts import render
from dj_rest_auth.registration.views import RegisterView
from .serializers import *
from .serializers import UserSerializer
from rest_framework import viewsets, status

class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):  # Sadece okuma izinli ViewSet
    queryset = get_user_model().objects.all()  # Tüm kullanıcıları getirir
    serializer_class = UserSerializer