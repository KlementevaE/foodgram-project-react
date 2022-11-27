import djoser.views as djoser_views
from django.urls import include, path, re_path
from rest_framework import routers
# isort: split
import api.views as views


router = routers.DefaultRouter()
router.register(r'ingredients', views.IngredientViewSet)
router.register(r'tags', views.TagViewSet)
router.register(r'recipes', views.RecipeViewSet, basename='recipe')
router.register(r'users', views.SubscribeViewSet, basename='subscribe')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    re_path(r'^auth/token/login/?$', views.CustomTokenCreateView.as_view(),
            name="login"),
    re_path(r'^auth/token/logout/?$', djoser_views.TokenDestroyView.as_view(),
            name="logout"),
]
