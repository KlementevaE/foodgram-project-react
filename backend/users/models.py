from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(
        verbose_name=_('email'),
        max_length=254,
    )
    username = models.CharField(
        verbose_name=_('username'),
        max_length=150,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name=_('first name'),
        max_length=150,
    )
    last_name = models.CharField(
        verbose_name=_('last name'),
        max_length=150,
    )
    password = models.CharField(
        verbose_name=_('password'),
        max_length=150,
    )

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-pk']

    def __str__(self):
        return self.username


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name=_('subsriber'),
        on_delete=models.CASCADE,
        related_name='subscriber',
    )
    author = models.ForeignKey(
        User,
        verbose_name=_('author'),
        on_delete=models.CASCADE,
        related_name='author',
    )

    class Meta:
        verbose_name = _('subscriptions')
        verbose_name_plural = _('subscriptions')
        ordering = ['-pk']
        constraints = [
            models.UniqueConstraint(fields=['user', 'author'],
                                    name='unique_subscribe'),
            models.CheckConstraint(check=~models.Q(author=models.F('user')),
                                   name='author_not_user'),
        ]

    def __str__(self):
        return f'{self.user} подписан на автора {self.author}'
