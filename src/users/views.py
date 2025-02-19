from django.contrib.auth.models import User
from rest_framework import generics

from .serializers import UserCreateSerializer


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
