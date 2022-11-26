import datetime

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser import utils
from djoser.conf import settings
from djoser.views import TokenCreateView, UserViewSet
from recipes.models import Cart, Favorite, Ingredient, Recipe, Tag
from rest_framework import permissions, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from users.models import Subscribe, User

from .filters import IngredientFilter, RecipeFilter
from .pagination import CustomPagination
from .permissions import IsAuthOrReadOnly
from .serializers import (CustomUserSerializer, IngredientSerializer,
                          RecipeCreateUpdateSerializer, RecipeReadSerializer,
                          RecipeSubscribeFavoriteCartSerializer,
                          SubscribeSerializer, TagSerializer)


class CustomTokenCreateView(TokenCreateView):
    """Переопределение view из djoser для изменения кода ответа Http."""

    def _action(self, serializer):
        token = utils.login_user(self.request, serializer.user)
        token_serializer_class = settings.SERIALIZERS.token
        return Response(
            data=token_serializer_class(token).data,
            status=status.HTTP_201_CREATED)


class SubscribeViewSet(UserViewSet):
    """Viewset для эндпоинтов
    users/{pk}/subcribe и users/subcriptions.
    """

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = CustomPagination

    @action(detail=True, methods=('POST', 'DELETE'),
            serializer_class=SubscribeSerializer)
    def subscribe(self, request, *args, **kwargs):
        user = self.request.user
        author_id = self.kwargs.get('id')
        author = get_object_or_404(User, pk=author_id)
        data = {'user': user, 'author': author}
        serializer = self.get_serializer(data=data)
        if request.method == 'POST':
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        subsribe = Subscribe.objects.filter(user=user, author=author)
        if not subsribe.exists():
            raise serializers.ValidationError("Такой подписки не существует")
        subsribe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, serializer_class=SubscribeSerializer,
            pagination_class=CustomPagination)
    def subscriptions(self, request):
        user = self.request.user
        new_queryset = user.subscriber.all()
        page = self.paginate_queryset(new_queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(new_queryset, many=True)
        return Response(serializer.data)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset для эндпоинта ingredients."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    pagination_class = None


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset для эндпоинта tags."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    """Viewset для эндпоинтов
    recipes, recipes/{pk}/favorite, recipes/{pk}/shopping_cart и
    recipes/download_shopping_cart.
    """

    queryset = Recipe.objects.all()
    pagination_class = CustomPagination
    permission_classes = (IsAuthOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action == 'favorite':
            return RecipeSubscribeFavoriteCartSerializer
        if self.action == 'shopping_cart':
            return RecipeSubscribeFavoriteCartSerializer
        method = self.request.method
        if method == 'GET':
            return RecipeReadSerializer
        return RecipeCreateUpdateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=('POST', 'DELETE'))
    def favorite(self, request, pk):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        data = {'user': user, 'recipe': recipe}
        serializer = self.get_serializer(recipe, data=data)
        if request.method == 'POST':
            if serializer.is_valid():
                if Favorite.objects.filter(user=user, recipe=recipe).exists():
                    raise serializers.ValidationError(
                        'Рецепт уже добавлен в избранное')
                Favorite.objects.create(user=user, recipe=recipe)
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        favorite = Favorite.objects.filter(user=user, recipe=recipe)
        if not favorite.exists():
            raise serializers.ValidationError('Такого рецепта нет в избранном')
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=('POST', 'DELETE'))
    def shopping_cart(self, request, pk):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        data = {'user': user, 'recipe': recipe}
        serializer = self.get_serializer(recipe, data=data)
        if request.method == 'POST':
            if serializer.is_valid():
                if Cart.objects.filter(user=user, recipe=recipe).exists():
                    raise serializers.ValidationError(
                        'Рецепт уже добавлен в корзину')
                Cart.objects.create(user=user, recipe=recipe)
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        cart = Cart.objects.filter(user=user, recipe=recipe)
        if not cart.exists():
            raise serializers.ValidationError('Такого рецепта нет в корзине')
        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, permission_classes=(permissions.IsAuthenticated,))
    def download_shopping_cart(self, request):
        sum_ingredients = Recipe.objects.filter(
            cart__user=self.request.user).values(
                'recipeingredient__ingredient__name',
                'recipeingredient__ingredient__measurement_unit').annotate(
                    amount=Sum('recipeingredient__amount'))
        nowtime = datetime.datetime.now().strftime("%d/%m/%Y")
        list_ingredients = f'Foodgram {nowtime}.\n'
        count = 1
        for ingredient in sum_ingredients:
            list_ingredients += (f'{count}. {ingredient[0]}: {ingredient[2]}'
                                 f' {ingredient[1]}\n')
            count += 1
        return HttpResponse(list_ingredients, content_type='text/plain')
