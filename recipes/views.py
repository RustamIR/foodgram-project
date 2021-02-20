from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from recipes.forms import RecipeForm
from recipes.models import Recipe, Tag
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
    return render(
        request,
        'singlePage.html',
        {'recipe':recipe, 'following': follow(request, recipe.author.username)}
    )


@login_required
def recipe_new(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        recipe = save_recipe(request, form)
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
        edit_recipe(request, form, instance=recipe)
        return redirect(
            'recipe_view_slug',
            recipe_id=recipe.id,
            slug=recipe.slug
        )
    return render(
        request,
        'formRecipe.html',
        {'form': form, 'recipe': recipe}
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
    paginator = Paginator(author_recipes, settings.PAGINATION_PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'authorRecipe.html',
        {
            'following': follow(request, username),
            'author': author,
            'page': page,
            'paginator': paginator,
            'tags': tags_filter(request),
            'all_tags': all_tags,
        }
    )


@login_required
def subscriptions(request):
    authors = User.objects.filter(following__user=request.user)
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
