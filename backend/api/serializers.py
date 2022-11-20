import base64

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from recipes.models import (Cart, Favorite, Ingredient, Recipe,
                            RecipeIngredient, Tag)
from users.models import Subscribe, User


class CustomUserSerializer(UserSerializer):
    """Сериализатор для модели User."""

    is_subscribed = serializers.SerializerMethodField()

    class Meta():
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed')

    def get_is_subscribed(self, obj):
        request = self.context['request']
        user = request.user
        author = obj
        if request.user.is_authenticated and Subscribe.objects.filter(
           user=user, author=author).exists():
            return True
        return False


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор при создании объекта модели User."""

    class Meta():
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'password')


class SubscribeSerializer(CustomUserSerializer):
    """Сериализатор для модели Subscribe."""

    email = serializers.CharField(source='author.email', read_only=True)
    id = serializers.CharField(source='author.id', read_only=True)
    username = serializers.CharField(source='author.username', read_only=True)
    first_name = serializers.CharField(
        source='author.first_name',
        read_only=True)
    last_name = serializers.CharField(
        source='author.last_name',
        read_only=True)
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField(source='author.recipes')
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')
        model = Subscribe

    def to_internal_value(self, data):
        super().to_internal_value(data)
        return data

    def validate(self, data):
        author = data['author']
        user = self.context.get('request').user
        if user == author:
            raise serializers.ValidationError('Нельзя подписаться на себя')
        if Subscribe.objects.filter(user=user, author=author).exists():
            raise serializers.ValidationError('Подписка уже существует')
        return data

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        author = obj.author
        if Subscribe.objects.filter(user=user, author=author).exists():
            return True
        return False

    def get_recipes(self, obj):
        request = self.context['request']
        recipes_limit = request.query_params.get('recipes_limit')
        if recipes_limit is None:
            recipes_limit = 6
        author = obj.author
        recipes = author.recipes.all()[:int(recipes_limit)]
        return RecipeSubscribeFavoriteCartSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        author = obj.author
        count = author.recipes.count()
        return count


class Base64ImageField(serializers.ImageField):
    """Сериализатор для декодирования картинки из base64."""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class RecipeSubscribeFavoriteCartSerializer(serializers.ModelSerializer):
    """Сериализатор модели Recipe
    используемый для Subscribe, Favorite, Cart.
    """

    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('name', 'cooking_time')
        model = Recipe


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Ingredient."""

    class Meta:
        fields = ('id', 'name', 'measurement_unit')
        model = Ingredient


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Tag."""

    class Meta:
        fields = ('id', 'name', 'color', 'slug')
        model = Tag


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для связанной модели RecipeIngredient."""

    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit',
        read_only=True)

    class Meta:
        fields = ('id', 'name', 'measurement_unit', 'amount')
        model = RecipeIngredient


class RecipeReadSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Recipe при GET-запросе."""
    tags = TagSerializer(many=True)
    ingredients = RecipeIngredientSerializer(
        many=True,
        source='recipeingredient')
    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField(required=False, allow_null=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')
        model = Recipe

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_authenticated and Favorite.objects.filter(
           user=user, recipe=obj).exists():
            return True
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_authenticated and Cart.objects.filter(
           user=user, recipe=obj).exists():
            return True
        return False


class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Recipe при запросах POST, PATCH, DELETE."""

    ingredients = RecipeIngredientSerializer(
        many=True,
        source='recipeingredient')
    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField(required=False, allow_null=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')
        model = Recipe

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if Favorite.objects.filter(user=user, recipe=obj).exists():
            return True
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if Cart.objects.filter(user=user, recipe=obj).exists():
            return True
        return False

    def validate(self, data):
        ingredients = data.get('recipeingredient')
        for ingredient in ingredients:
            id = ingredient.get('ingredient').get('id')
            if not Ingredient.objects.filter(pk=id).exists():
                raise serializers.ValidationError(f'Такого ингредиента id={id}'
                                                  ' в базе нет')
            if ingredient.get('amount') < 1:
                raise serializers.ValidationError('Количество ингредиента'
                                                  ' должно быть больше 0')
        if data.get('cooking_time') < 1:
            raise serializers.ValidationError('Время приготовления должно быть'
                                              ' больше 0')
        return data

    def create_ingredients(self, ingredients, recipe):
        ingredient_ids = []
        for ingredient in ingredients:
            current_ingredient = get_object_or_404(
                Ingredient,
                pk=ingredient.get('ingredient').get('id'))
            amount = ingredient.get('amount')
            RecipeIngredient.objects.create(
                ingredient=current_ingredient,
                recipe=recipe,
                amount=amount)
            ingredient_ids.append(current_ingredient.pk)
        return ingredient_ids

    def update_ingredients(self, ingredients, instance):
        ingredient_ids = []
        RecipeIngredient.objects.filter(recipe=instance).delete()
        for ingredient in ingredients:
            pk = ingredient.get('ingredient').get('id')
            amount = ingredient.get('amount')
            current_ingredient = get_object_or_404(Ingredient, pk=pk)
            RecipeIngredient.objects.create(
                recipe=instance,
                ingredient=current_ingredient,
                amount=amount
                )
            ingredient_ids.append(current_ingredient.pk)
        return ingredient_ids

    def update_tags(self, tags):
        tag_id = []
        for tag in tags:
            tag_id.append(tag.id)
        return tag_id

    def create(self, validated_data):
        ingredients = validated_data.pop('recipeingredient')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.save()
        recipe.tags.add(*tags)
        recipe.ingredients.set(self.create_ingredients(ingredients, recipe))
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', [])
        ingredients = validated_data.pop('recipeingredient', [])
        instance.ingredients.set(
            self.update_ingredients(ingredients, instance))
        instance.tags.set(self.update_tags(tags))
        fields = ['name', 'image', 'text', 'cooking_time']
        for field in fields:
            try:
                setattr(instance, field, validated_data[field])
            except KeyError as exc:
                print(f'Ошибка валидации: {exc}')
        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        tags = instance.tags.all()
        i = 0
        for tag in tags:
            representation['tags'][i] = {'id': tag.id,
                                         'name': tag.name,
                                         'color': tag.color,
                                         'slug': tag.slug}
            i += 1
        return representation
