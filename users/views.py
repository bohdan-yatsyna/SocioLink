from django.shortcuts import get_object_or_404
from rest_framework import generics, exceptions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import User
from users.serializers import (
    CustomTokenObtainPairSerializer,
    UserLastActivitySerializer,
    UserSerializer,
)


class SignupUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserLastActivityView(generics.RetrieveAPIView):
    serializer_class = UserLastActivitySerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        user_id = self.kwargs["user_id"]
        user = get_object_or_404(User, id=user_id)

        if self.request.user == user or self.request.user.is_superuser:
            return user

        raise exceptions.PermissionDenied(
            detail="Access denied, you can not see this user's activity."
        )
