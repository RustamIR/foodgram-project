from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum, Count
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django import forms

from api.models import Subscribe
from recipes.forms import RecipeForm
from recipes.models import Recipe, Tag, Ingredient
from recipes.utils import edit_recipe, save_recipe, tags_filter, follow


User = get_user_model()


def index(request):
    all_tags = Tag.objects.all()
    select_tags = tags_filter(request)
    recipes = Recipe.objects.filter(
            tags__title__in=select_tags
        ).select_related(
            'author'
        ).prefetch_related(
            'tags'
        ).distinct()
    paginator = Paginator(recipes, settings.PAGINATION_PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'page': page,
        'paginator': paginator,
        'tags': select_tags,
        'all_tags': all_tags
    }
    return render(request, 'index.html', context)


def recipe_view_redirect(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render('recipe_view_slug', recipe_id=recipe.id, slug=recipe.slug)


def recipe_view_slug(request, recipe_id, slug):
    recipe = get_object_or_404(
        Recipe.objects.select_related('author'),
        id=recipe_id,
        slug=slug,
    )
    following = False
    if Subscribe.objects.filter(
            user__username=request.user.username,
            author__username=recipe.author.username
    ).exists():
        following = True
    return render(
        request,
        'singlePage.html',
        {'recipe':recipe, 'following': following}
    )


@login_required
def recipe_new(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        try:
            recipe = save_recipe(request, form)
        except forms.ValidationError as e:
            return render(
                request,
                'formRecipe.html',
                {'form': form,
                 'errortext': str(e)}
            )
        return redirect(
            'recipe_view_slug',
            recipe_id=recipe.id,
            slug=recipe.slug
        )

    return render(
        request,
        'formRecipe.html',
        {'form': form}
    )


@login_required
def recipe_edit(request, recipe_id, slug):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    # ing = recipe.ingredients.all()    # вытащить ингрединеты и передать их а отдельную переменную и распечать ее в шаблоне
    # ing = Ingredient.objects.filter(recipe=recipe).all()
    if not request.user.is_superuser:
        if request.user != recipe.author:
            return redirect(
                'recipe_view_slug',
                recipe_id=recipe.id,
                slug=recipe.slug
            )
    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipe
    )
    if form.is_valid():
        try:
            recipe = edit_recipe(request, form, instance=recipe)
        except forms.ValidationError as e:
            return render(
                request,
                'formRecipe.html',
                {'form': form,
                 # 'ing': ing,
                 'errortext': str(e)}
            )
        return redirect(
            'recipe_view_slug',
            recipe_id=recipe.id,
            slug=recipe.slug
        )
    return render(
        request,
        'formRecipe.html',
        {
            'form': form,
            'recipe': recipe,
            # 'ing': ing
         }
    )


@login_required
def recipe_delete(request, recipe_id, slug):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user.is_superuser or request.user == recipe.author:
        recipe.delete()
    return redirect('index')


def profile_view(request, username):
    all_tags = Tag.objects.all()
    author = get_object_or_404(User, username=username)
    author_recipes = author.author_recipes.filter(
        tags__title__in=tags_filter(request)
    ).prefetch_related('tags').distinct()
    following = False
    if Subscribe.objects.filter(
            user__username=request.user.username,
            author__username=username
    ).exists():
        following = True
    paginator = Paginator(author_recipes, settings.PAGINATION_PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'authorRecipe.html',
        {
            'following': following,
            'author': author,
            'page': page,
            'paginator': paginator,
            'tags': tags_filter(request),
            'all_tags': all_tags,
        }
    )


@login_required
def subscriptions(request):
    authors = User.objects.filter(
        following__user=request.user
    ).prefetch_related(
        'author_recipes'
    ).annotate(recipe_count=Count('author_recipes')).order_by('username')
    paginator = Paginator(authors, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request, 'myFollow.html', {'page': page, 'paginator': paginator}
    )


@login_required
def favorites(request):
    all_tags = Tag.objects.all()
    recipes = Recipe.objects.filter(
        favored_by__user=request.user,
        tags__title__in=tags_filter(request)
    ).select_related(
        'author'
    ).prefetch_related(
        'tags'
    ).distinct()

    paginator = Paginator(recipes, settings.PAGINATION_PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        'favorite.html',
        {
            'page': page,
            'paginator': paginator,
            'tags': tags_filter(request),
            'all_tags': all_tags,
        }
    )


@login_required
def purchases(request):
    recipes = request.user.purchases.all()
    return render(
        request,
        'shopList.html',
        {'recipes': recipes},
    )


def get_ingredients(request):
    text = ''
    list_ingredients = (
        Recipe.objects.filter(in_purchases__user=request.user)
        .order_by("ingredients__title")
        .values("ingredients__title", "ingredients__dimension")
        .annotate(amount=Sum("ingredients_amounts__quantity"))
    )

    for ingredient in list_ingredients:
        text += (
            f"{ingredient['ingredients__title']} "
            f"({ingredient['ingredients__dimension']})"
            f" \u2014 {ingredient['amount']} \n"
        )

    filename = "ingredients.txt"
    response = HttpResponse(text, content_type="text/plain")
    response['Content-Disposition'] = 'attachment; filename={0}'.format(
        filename
    )
    return response
