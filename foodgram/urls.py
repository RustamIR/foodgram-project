from django.contrib import admin
from django.urls import include, path

from . import views

handler404 = 'foodgram.views.page_not_found'    #noqa
handler500 = 'foodgram.views.server_error'  #noqa


flatpages_urls = [
    path('author/', views.AboutView.as_view(), name='author'),
    path('spec/', views.SpecView.as_view(), name='spec'),
]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('about/', include(flatpages_urls)),
    path('api/v1/', include('api.urls')),
    path('', include('recipes.urls')),
]

urlpatterns += [
    path('404/', views.page_not_found, name='404'),
    path('500/', views.server_error, name='500'),
]

