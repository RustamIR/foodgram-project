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
    path('follow/', views.subscriptions, name='subscriptions'),
    path('favorites/', views.favorites, name='favorites'),
    path('purchases/', views.purchases, name='purchases'),
    path('<str:username>/', views.profile_view, name='profile_view'),
]
    # path('<str:username>/unfollow/', views.profile_unfollow,
    #      name='profile_unfollow'),
    # path('<str:username>/follow/', views.profile_follow,
    #      name='profile_follow'),
    # path('<int:recipe_id>/<slug:slug>/single_page_unfollow/', views.single_page_unfollow,
    #      name='single_page_unfollow'),
    # path('<int:recipe_id>/<slug:slug>/single_page_follow/', views.single_page_follow,
    #      name='single_page_follow'),
    # path('favorites/', views.favorites, name='favorites'),
    # path('purchases/', views.purchases, name='purchases'),
    # path('download/', views.purchases_download, name='purchases_download'),
    # path('<str:username>/', views.profile_view, name='profile_view'),
    # path("subscriptions/<int:id>/",
    #      views.profile_unfollow, name="profile_unfollow"),
    # path("subscriptions/<str:username>", views.profile_follow, name="profile_follow"),
    # path('shoplist/', views.download, name='shoplist'),

