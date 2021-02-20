from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.recipe_new, name='recipe_new'),
    path(
        '<int:recipe_id>/<slug:slug>/',
        views.recipe_view_slug,
        name='recipe_view_slug',
    ),
    path(
        '<int:recipe_id>/',
        views.recipe_view_redirect,
        name='recipe_view_redirect',
    ),
    path('<int:recipe_id>/<slug:slug>/edit/',
         views.recipe_edit, name='recipe_edit'),
    path(
        '<int:recipe_id>/<slug:slug>/delete/',
        views.recipe_delete,
        name='recipe_delete',
    ),
    path('subscriptions/', views.subscriptions, name='subscriptions'),
    path('favorites/', views.favorites, name='favorites'),
    path('purchases/', views.purchases, name='purchases'),
    path('shoplist/', views.get_ingredients, name='shoplist'),
    path('<str:username>/', views.profile_view, name='profile_view'),
]
