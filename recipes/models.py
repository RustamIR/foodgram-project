from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Q, F
from django.utils.safestring import mark_safe
from django_extensions.db.fields import AutoSlugField


User = get_user_model()


class Ingredient(models.Model):
    title = models.CharField('Название ингредиента', max_length=200, db_index=True, unique=True)
    dimension = models.CharField(verbose_name='Eдиница измерения', max_length=50)

    class Meta:
        ordering = ('title', )
        verbose_name = "Ингридиент"
        verbose_name_plural = "Ингридиенты"

    def __str__(self):
        return f'{self.title}, {self.dimension}'


class Recipe(models.Model):
    title = models.CharField('Название рецепта', max_length = 200, blank=False)
    text = models.TextField('Описание', blank=False)
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        validators=[MinValueValidator(1)]
    )
    slug = AutoSlugField(populate_from='title', allow_unicode=True)
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
        )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author_recipes',
        verbose_name='Автор'
        )
    tags = models.ManyToManyField(
        'Tag',
        related_name='recipes',
        verbose_name = 'Теги'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        related_name='ingredients',
        verbose_name='Ингридиент'
        )
    image = models.ImageField('Изображение', upload_to='images/')

    # def __str__(self):
    #     return Truncator(self.text).chars(1000)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return self.title

    # @property
    # def favorite_count(self):
    #     return self.recipe_amount.count()
    #
    # def image_img(self):
    #     if self.image:
    #         return mark_safe(f'<img width="90" height="50" src="{self.image.url}" />')
    #     return 'Без изображения'
    #
    # image_img.short_description = 'изображение'


class Tag(models.Model):
    title = models.CharField('Имя тега', max_length=50, db_index=True)
    display_name = models.CharField('Имя тега для шаблона', max_length=50)
    color = models.CharField('Цвет тега', max_length=50)

    class Meta:
        verbose_name='тег'
        verbose_name_plural='теги'

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients_amounts'
    )
    quantity = models.DecimalField(
        max_digits=6,
        decimal_places=1,
        validators=[MinValueValidator(1)]
    )

    class Meta:
        unique_together = ('ingredient', 'recipe')
        verbose_name = 'Рецепт - Ингредиент'
        verbose_name_plural = 'Рецепты - Ингредиенты'

    # def __str__(self):
    #     return f'Из рецепта "{self.recipe}"'


# class Subscribe(models.Model):
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='follower',
#         verbose_name='Пользователь',
#     )
#     author = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='following',
#         verbose_name='Автор'
#     )
#
#     def save(self, **kwargs):
#         if self.user != self.author:
#             super(Subscribe, self).save(**kwargs)
#
#     def __str__(self):
#         return f"{self.user.username} follow to {self.author.username}"
#
#     class Meta:
#         constraints = [
#             models.UniqueConstraint(
#                 fields=['user', 'author'],
#                 name='unique_user_author'
#             ),
#             models.CheckConstraint(
#                 check=~Q(user=F('author')),
#                 name='user_not_author',
#             )
#         ]
#
#     class Meta:
#         verbose_name = 'Подписка'
#         verbose_name_plural = 'Подписки'
#         unique_together = ('user', 'author')
#
#
# class Favorite(models.Model):
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='favorites',
#         verbose_name='Пользователь',
#     )
#     recipe = models.ForeignKey(
#         Recipe,
#         on_delete=models.CASCADE,
#         related_name='favored_by',
#         verbose_name='Рецепт в избранном',
#     )
#
#     class Meta:
#         verbose_name = 'Избраннцй рецепт'
#         verbose_name_plural = 'Избранные рецепты'
#
#
# class Purchase(models.Model):
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='purchases',
#         verbose_name='Пользователь',
#     )
#     recipe = models.ForeignKey(
#         Recipe,
#         on_delete=models.CASCADE,
#         verbose_name='Рецепт',
#     )
#
#     class Meta:
#         unique_together = ('user', 'recipe')
#         verbose_name = 'Список покупок'
#         verbose_name_plural = 'Списки покупок'
