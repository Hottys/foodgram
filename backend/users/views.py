from api.users_api.serializers import SubscribeSerializer, UserSerializer
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Subscribe

User = get_user_model()


class UserViewSet(UserViewSet):
    """Работа с пользователями."""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(
        detail=True,
        methods=['POST'],
        permission_classes=[IsAuthenticated],
    )
    def subscribe(self, request, id):
        author = get_object_or_404(User, pk=id)
        sub = Subscribe.objects.filter(
            user=request.user, author=author)
        if sub:
            return Response(
                {'errors': 'Вы уже подписаны на этого пользователя!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if author == request.user:
            return Response(
                {'errors': 'Нельзя подписаться на самого себя!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        Subscribe.objects.create(user=request.user, author=author)
        serializer = SubscribeSerializer(
            author, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def delete_subscribe(self, request, id):
        author = get_object_or_404(User, pk=id)
        sub = Subscribe.objects.filter(user=request.user, author=author)
        if not sub:
            return Response(
                {'errors': 'Невозможно удалить несуществующую подписку.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        sub.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def subscriptions(self, request):
        user = request.user
        queryset = User.objects.filter(subscribing__user=user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscribeSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
