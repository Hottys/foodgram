from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.recipes_api.serializers import TagSerializer

from .models import Tag


class TagViewSet(ReadOnlyModelViewSet):
    """Вывод тегов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    pagination_class = None
