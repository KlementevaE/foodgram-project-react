from django.contrib import admin

from .models import Cart, Favorite, Ingredient, Recipe, RecipeIngredient, Tag


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    list_filter = ('name',)


admin.site.register(Ingredient, IngredientAdmin)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'name', 'count_favorite')
    list_filter = ('author', 'name', 'tags')

    def count_favorite(self, obj):
        return obj.favorite.count()


admin.site.register(Recipe, RecipeAdmin)


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')


admin.site.register(Tag, TagAdmin)


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe_id', 'ingredient_id', 'amount')


admin.site.register(RecipeIngredient, RecipeIngredientAdmin)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user_id', 'recipe_id')


admin.site.register(Favorite, FavoriteAdmin)


class CartAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user_id', 'recipe_id')


admin.site.register(Cart, CartAdmin)
