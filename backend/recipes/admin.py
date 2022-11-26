from django.contrib import admin

from .models import Cart, Favorite, Ingredient, Recipe, RecipeIngredient, Tag


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    list_filter = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'name', 'count_favorite')
    list_filter = ('author', 'name', 'tags')

    def count_favorite(self, obj):
        return obj.favorite.count()


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe_id', 'ingredient_id', 'amount')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user_id', 'recipe_id')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user_id', 'recipe_id')
