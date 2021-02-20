from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django_extensions.db.fields import AutoSlugField

User = get_user_model()


class Ingredient(models.Model):
    title = models.CharField(
        'Название ингредиента',
        max_length=200,
        db_index=True,
        unique=True
    )
    dimension = models.CharField(
        verbose_name='Eдиница измерения',
        max_length=50
    )

    class Meta:
        ordering = ('title', )
        verbose_name = "Ингридиент"
        verbose_name_plural = "Ингридиенты"

    def __str__(self):
        return f'{self.title}, {self.dimension}'


class Recipe(models.Model):
    title = models.CharField(
        'Название рецепта',
        max_length = 200,
        blank=False
    )
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
        verbose_name='Ингридиент'
        )
    image = models.ImageField('Изображение', upload_to='images/')

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return self.title


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
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='ing')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients_amounts'
    )
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique_ingredient_recipe'
            )
        ]
        verbose_name = 'Рецепт - Ингредиент'
        verbose_name_plural = 'Рецепты - Ингредиенты'
