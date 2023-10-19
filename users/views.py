from django.utils import timezone
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from users.serializers import UserSerializer, UserLastActivitySerializer, CustomTokenObtainPairSerializer


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
        return self.request.user
