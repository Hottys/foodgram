from api.serializers import UserSerializer
from djoser.views import UserViewSet
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet
from users.models import User

from .models import User


class UserViewSet(UserViewSet):
    """Работа с моделью пользователя."""
    queryset = User.objects.all()
    serializer_class = UserSerializer

