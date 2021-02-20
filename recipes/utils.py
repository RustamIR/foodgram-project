from decimal import Decimal

from django import forms
from django.db import IntegrityError, transaction
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404

from api.models import Subscribe
from .models import Ingredient, RecipeIngredient
# from .utils import get_ingredients_from_form


BREAKFAST = 'breakfast'
LUNCH = 'lunch'
DINNER = 'dinner'
TAGS = [BREAKFAST, LUNCH, DINNER]


def tags_filter(request):
    tags = request.GET.getlist('tag', TAGS)
    return tags


def follow(request, username):
    following = False
    if Subscribe.objects.filter(
            user__username=request.user.username,
            author__username=username
    ).exists():
        following = True
    return following


def get_add_ingredients(request):
    ingredients = {}
    for key, name in request.POST.items():
        if key.startswith('nameIngredient'):
            num = key.split('_')[1]
            ingredients[name] = request.POST[
                f'valueIngredient_{num}'
            ]

    return ingredients

def get_ingredients_from_form(ingredients, recipe):
    ingredients = []
    for ingredient in ingredients:
        product = get_object_or_404(Ingredient, title=ingredient['title'])
        ingredients.append(
            Ingredient(recipe=recipe, ingredient=product,
                       amount=ingredient['amount']))
    return ingredients


def save_recipe(request, form):
    try:
        with transaction.atomic():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()

            objs = []
            ingredients = get_add_ingredients(request)
            for name, quantity in ingredients.items():
                ingredient = get_object_or_404(Ingredient, title=name)
                if int(quantity) > 0:
                    objs.append(
                        RecipeIngredient(
                            recipe=recipe,
                            ingredient=ingredient,
                            quantity=int(quantity)
                        )
                    )
                else:
                    raise forms.ValidationError('Количество ингредиентов должно быть больше нуля')

            RecipeIngredient.objects.bulk_create(objs)

            form.save_m2m()
            return recipe
    except IntegrityError:
        raise HttpResponseBadRequest


def edit_recipe(request, form, instance):
    try:
        with transaction.atomic():
            RecipeIngredient.objects.filter(recipe=instance).delete()
            return save_recipe(request, form)
    except IntegrityError:
        raise HttpResponseBadRequest


