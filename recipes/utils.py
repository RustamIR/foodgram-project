from decimal import Decimal
from sqlite3 import IntegrityError

from django.db import transaction
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from recipe import Ingredient
from .models import RecipeIngredient


def get_ingredients(request):
    """
    Parse POST request body for ingredient names and their respective amounts.
    """
    ingredients = {}
    for key, name in request.POST.items():
        if key.startswith('nameIngredient'):
            num = key.split('_')[1]
            ingredients[name] = request.POST[
                f'valueIngredient_{num}'
            ]

    return ingredients


def save_recipe(request, form):
    """
    Create and save a Recipe instance with neccessary m2m relationships.
    """
    try:
        with transaction.atomic():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()

            objs = []
            ingredients = get_ingredients(request)
            for name, quantity in ingredients.items():
                ingredient = get_object_or_404(Ingredient, title=name)
                objs.append(
                    RecipeIngredient(
                        recipe=recipe,
                        ingredient=ingredient,
                        quantity=Decimal(quantity.replace(',', '.'))
                    )
                )
            RecipeIngredient.objects.bulk_create(objs)

            form.save_m2m()
            return recipe
    except IntegrityError:
        raise HttpResponseBadRequest


