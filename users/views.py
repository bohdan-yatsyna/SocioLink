from django.shortcuts import get_object_or_404
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)
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
    """
    View for Person registering on the portal, Authentication is not required.
    """

    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


# Only for documentation endpoints details
@extend_schema_view(
    get=extend_schema(
        description="Endpoint with detailed User page for current user."
    ),
    put=extend_schema(
        description="Endpoint for updating current User details by id."
    ),
    patch=extend_schema(
        description="Endpoint for partial updating "
                    "current User details by id."
    ),
    delete=extend_schema(
        description="Endpoint for deleting current User account by id."
    )
)
class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class CustomTokenObtainPairView(TokenObtainPairView):
    """Responsible for user login and for handling 'last_login' data"""

    serializer_class = CustomTokenObtainPairSerializer


class UserLastActivityView(generics.RetrieveAPIView):
    """
    Endpoint purposed to show user last login and last request information.
    Only user himself or admin user can access such data by user id.
    """
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
