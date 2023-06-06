from io import BytesIO

from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.permissions import AuthorsPermission
from api.recipes_api.filters import FilterRecipe
from api.recipes_api.serializers import (RecipeCreateSerializer,
                                         RecipeFavoriteSerializer,
                                         RecipeSerializer,
                                         ShoppingListSerializer)
from recipes.models import (FavoriteRecipe, IngredientInRecipe, Recipe,
                            ShoppingList)

User = get_user_model()


class RecipeViewSet(ModelViewSet):
    """Работа с рецептами."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeCreateSerializer
    permission_classes = (AuthorsPermission, )
    filter_backends = (DjangoFilterBackend, )
    filterset_class = FilterRecipe

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeSerializer
        return RecipeCreateSerializer

    @staticmethod
    def create_shopping_cart(ingredients, user):
        buffer = BytesIO()
        p = canvas.Canvas(buffer)
        pdfmetrics.registerFont(
            TTFont('DejaVuSans', 'api/recipes_api/fonts/DejaVuSans.ttf')
        )
        p.setFont('DejaVuSans', 16)
        p.drawCentredString(
            300, 750, f'Список покупок для пользователя {user}'
        )
        x = 100
        y = 700
        p.setFont('DejaVuSans', 12)
        for ingredient in ingredients:
            name = ingredient['ingredient__name']
            measurement_unit = ingredient['ingredient__measurement_unit']
            value = ingredient['ingredient_value']
            text = f'{name} ({measurement_unit}) - {value}'
            p.drawString(x, y, text)
            y -= 20
        p.showPage()
        p.save()
        buffer.seek(0)
        pdf = buffer.getvalue()
        buffer.close()
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = (
            'attachment; filename="shopping_list.pdf'
        )
        response.write(pdf)
        return response

    @action(detail=False, methods=['GET'])
    def download_shopping_cart(self, request):
        user = request.user
        ingredients = IngredientInRecipe.objects.filter(
            recipe__shopping_list__user=request.user
        ).order_by('ingredient__name').values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(ingredient_value=Sum('amount'))
        return self.create_shopping_cart(ingredients, user)

    @action(detail=True, methods=['POST'])
    def shopping_cart(self, request, pk):
        return self.post_method_for_actions(
            request, pk, serializers=ShoppingListSerializer
        )

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        return self.delete_method_for_actions(
            request=request, pk=pk, model=ShoppingList)

    @action(detail=True, methods=['POST'])
    def favorite(self, request, pk):
        return self.post_method_for_actions(
            request=request, pk=pk, serializers=RecipeFavoriteSerializer)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        return self.delete_method_for_actions(
            request=request, pk=pk, model=FavoriteRecipe)

    @staticmethod
    def post_method_for_actions(request, pk, serializers):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = serializers(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def delete_method_for_actions(request, pk, model):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        model_instance = get_object_or_404(model, user=user, recipe=recipe)
        model_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
