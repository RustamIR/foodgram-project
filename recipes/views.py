import json

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Tag, Recipe
from .utils import save_recipe
from django.conf import settings
from .forms import RecipeForm
from api.models import Subscribe, Favorite, Purchase



User = get_user_model()
TAGS = ['breakfast', 'lunch', 'dinner']


def index(request):
    tags = request.GET.getlist('tag', TAGS)
    all_tags = Tag.objects.all()
    recipes = Recipe.objects.filter(tags__title__in = tags).distinct()
    paginator = Paginator(recipes, settings.PAGINATION_PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'page': page,
        'paginator': paginator,
        'tags': tags,
        'all_tags': all_tags
    }
    return render(request, 'index.html', context)


def recipe_view_redirect(request, recipe_id):
    recipe = get_object_or_404(Recipe.objects.all(), id=recipe_id)
    return render('recipe_view_slug', recipe_id=recipe.id, slug=recipe.slug)


def recipe_view_slug(request, recipe_id, slug):
    recipe =get_object_or_404(
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
    return render(request, 'singlePage.html', {'recipe':recipe, 'following': following}) # 'following':following


def recipe_new(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        recipe = save_recipe(request, form)
        return redirect('recipe_view_slug', recipe_id=recipe.id, slug=recipe.slug)
    return render(request, 'formRecipe.html', {'form': form})


@login_required
def recipe_edit(request, recipe_id, slug):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if not request.user.is_superuser:
        if request.user != recipe.author:
            return redirect('recipe_view_slug', recipe_id=recipe.id, slug=recipe.slug)
    form = RecipeForm(request.POST or None, files=request.FILES or None, instance=recipe)
    if form.is_valid():
        form.save()
        return redirect('recipe_view_slug', recipe_id=recipe.id, slug=recipe.slug)
    return render(request, 'formRecipe.html', {'form':form, 'recipe': recipe})


@login_required
def recipe_delete(request, recipe_id, slug):
    """
    Delete the given `recipes.Recipe`.
    """
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user.is_superuser or request.user == recipe.author:
        recipe.delete()
    return redirect('index')


def profile_view(request, username):
    tags = request.GET.getlist('tag', TAGS)
    all_tags = Tag.objects.all()
    author = get_object_or_404(User, username=username)
    author_recipes = author.author_recipes.filter(
        tags__title__in=tags
    ).prefetch_related('tags').distinct()
    paginator = Paginator(author_recipes, settings.PAGINATION_PAGE_SIZE)
    following = False
    if Subscribe.objects.filter(
            user__username=request.user.username,
            author__username=username
    ).exists():
        following = True
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
            'tags': tags,
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


# @login_required
# def profile_follow(request, username):
#     author = get_object_or_404(User, username=username)
#     if request.user != author:
#         Subscribe.objects.get_or_create(user=request.user, author=author)
#     return redirect("profile_view" , username=username)


# @login_required
# def single_page_follow(request,  recipe_id, slug):
#     recipe = get_object_or_404(
#         Recipe.objects.select_related('author'),
#         id=recipe_id,
#         slug=slug,
#     )
#     author = get_object_or_404(User, username=recipe.author.username)
#     if request.user != author:
#         Subscribe.objects.get_or_create(user=request.user, author=author)
#     return redirect("recipe_view_slug" , username=recipe.author.username)


# @login_required
# def single_page_unfollow(request, recipe_id, slug):
#     """Дизлайк отписка"""
#     recipe = get_object_or_404(
#         Recipe.objects.select_related('author'),
#         id=recipe_id,
#         slug=slug,
#     )
#     user = request.user
#     Subscribe.objects.filter(user=user, author=recipe.author).delete()
#     return redirect("recipe_view_slug", username=recipe.author.username)


# @login_required
# def profile_unfollow(request, username):
#     """Дизлайк отписка"""
#     author = get_object_or_404(User, username=username)
#     user = request.user
#     Subscribe.objects.filter(user=user, author=author).delete()
#     return redirect("profile_view", username=username)


# @login_required
# def profile_follow(request):
#     id = json.loads(request.body).get("id")
#     author = get_object_or_404(User, id=id)
#     if author == request.user:
#         return JsonResponse({"success": False})
#     follower = Subscribe.objects.get_or_create(user=request.user)
#     follower[0].author.add(author)
#     return JsonResponse({"success": True})
#
#
# @login_required
# def profile_unfollow(request, id):
#     profile = get_object_or_404(User, id=id)
#     follows = get_object_or_404(Subscribe, user=request.user)
#     follows.author.remove(profile)
#     return JsonResponse({"success": True})



@login_required
def favorites(request):
    """
    Display all `recipes.Recipe` that visitor had marked as favorite,
    filtered with tags.
    """
    tags = request.GET.getlist('tag', TAGS)
    all_tags = Tag.objects.all()
    recipes = Recipe.objects.filter(
        favored_by__user=request.user,
        tags__title__in=tags
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
            'tags': tags,
            'all_tags': all_tags,
        }
    )




@login_required
def purchases(request):
    """
    Display all `recipes.Recipe` the visitor had put in their shoplist.
    """
    recipes = request.user.purchases.all()
    return render(
        request,
        'shopList.html',
        {'recipes': recipes},
    )


# def purchases_dowload(request):
#     ingredients = request.user.purchases.select_related(
#         'recipe'
#     ).order_by(
#         'recipe__ingredients__title'
#     ).



# def profile_view(request, username):
#     """
#     Display all `recipes.Recipe` of a given `auth.User`, filtered with tags,
#     6 per page.
#     """
#     tags = request.GET.getlist('tag', TAGS)
#     all_tags = Tag.objects.all()
#
#     author = get_object_or_404(User, username=username)
#     author_recipes = author.recipes.filter(
#         tags__title__in=tags
#     ).prefetch_related('tags').distinct()
#
#     paginator = Paginator(author_recipes, settings.PAGINATION_PAGE_SIZE)
#     page_number = request.GET.get('page')
#     page = paginator.get_page(page_number)
#
#     return render(
#         request,
#         'authorRecipe.html',
#         {
#             'author': author,
#             'page': page,
#             'paginator': paginator,
#             'tags': tags,
#             'all_tags': all_tags,
#         }
#     )