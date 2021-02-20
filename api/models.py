from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import F, Q

from recipes.models import Recipe

User = get_user_model()


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Пользователь',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    def __str__(self):
        return f"{self.user.username} follow to {self.author.username}"

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_user_author'
            ),
            models.CheckConstraint(
                check=~Q(user=F('author')),
                name='user_not_author',
            )
        ]


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favored_by',
        verbose_name='Рецепт в избранном',
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'


class Purchase(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='purchases',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='in_purchases',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_recipe'
            ),
            models.CheckConstraint(
                check=~Q(user=F('recipe')),
                name='recipe_not_repite',
            )
        ]
