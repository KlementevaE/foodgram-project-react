from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
# isort: skip
from users.models import User

COLOR_PALETTE = [
    ('#E26C2D', 'orange', ),
    ('#86D83B', 'green', ),
    ('#790CD4', 'purple', ),
]


class Tag(models.Model):

    name = models.CharField(
        verbose_name=_('name'),
        max_length=200,
    )
    color = models.CharField(
        verbose_name=_('color in HEX'),
        max_length=7,
        choices=COLOR_PALETTE,
        default='#E26C2D',
    )
    slug = models.SlugField(
        verbose_name=_('slug'),
        max_length=200,
        null=True,
        unique=True,
    )

    class Meta:
        verbose_name = _('tag')
        verbose_name_plural = _('tags')
        ordering = ['name']

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name=_('name'),
        max_length=200,
        db_index=True,
    )
    measurement_unit = models.CharField(
        verbose_name=_('unit of measurement'),
        max_length=200,
    )

    class Meta:
        verbose_name = _('ingredient')
        verbose_name_plural = _('ingredients')
        ordering = ['name']

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name=_('author'),
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    name = models.CharField(
        verbose_name=_('name'),
        max_length=200,
    )
    image = models.ImageField(
        verbose_name=_('image'),
        upload_to='recipes/',
    )
    text = models.TextField(
        verbose_name=_('text'),
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name=_('ingredients'),
        through='RecipeIngredient',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name=_('tags'),
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name=_('cooking time'),
        validators=[MinValueValidator(1)],
    )
    pub_date = models.DateTimeField(
        verbose_name=_('date of publication'),
        auto_now_add=True,
    )

    class Meta:
        verbose_name = _('recipe')
        verbose_name_plural = _('recipes')
        ordering = ['-pub_date']

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        verbose_name=_('recipe'),
        on_delete=models.CASCADE,
        related_name='recipeingredient',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name=_('ingredient'),
        on_delete=models.CASCADE,
        related_name='amount',
    )
    amount = models.PositiveIntegerField(
        verbose_name=_('amount'),
        validators=[MinValueValidator(1)],
    )

    class Meta:
        verbose_name = _('recipe and ingredient'),
        verbose_name_plural = verbose_name,
        ordering = ['-pk']
        constraints = [
            models.UniqueConstraint(fields=['recipe', 'ingredient'],
                                    name='unique_connection_ri'),
        ]


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name=_('user'),
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name=_('recipe'),
        on_delete=models.CASCADE,
        related_name='favorite',
    )

    class Meta:
        verbose_name = _('favourites')
        verbose_name_plural = _('favourites')
        ordering = ['-pk']
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_favorite'),
        ]

    def __str__(self):
        return f'{self.recipe} in favourites {self.user}'


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name=_('user'),
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name=_('recipe'),
        on_delete=models.CASCADE,
        related_name='cart',
    )

    class Meta:
        verbose_name = _('shopping cart')
        verbose_name_plural = _('shopping cart')
        ordering = ['-pk']
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_cart'),
        ]

    def __str__(self):
        return f'{self.recipe} in shopping cart {self.user}'
