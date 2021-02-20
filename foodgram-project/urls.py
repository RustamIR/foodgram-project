from django.contrib.flatpages import views
from django.conf.urls import handler404, handler500
from django.conf import settings
from django.conf.urls.static import static

from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_view
from django.contrib.flatpages.views import flatpage
from django.urls import include, path


# handler400 = 'foodgram.views.page_bad_request'
# handler404 = 'foodgram.views.page_not_found'
# handler500 = 'foodgram.views.server_error'

flatpages_urls = [
    path('', flatpage, {'url': '/author/'}, name='about_author'),
    path('', flatpage, {'url': '/tech/'}, name='about_tech'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('about/', include(flatpages_urls)),
    path('', include('recipes.urls')),
    path('', include('api.urls')),
]


urlpatterns += [
    path('auth/', include([
            path('login/', auth_view.LoginView.as_view(
                template_name='registration/reg.html'), name='login'),
            path('logout/', auth_view.LogoutView.as_view(
                template_name='registration/logged_out.html'), name='logout'),
            path('password-change/', auth_view.PasswordChangeView.as_view(
                template_name='registration/password_change_form.html'
            ), name='password_change'),
            path('password-change/done/',
                 auth_view.PasswordChangeDoneView.as_view(
                    template_name='registration/password_change_done.html'
                    ), name='password_change_done'),
            path(
                'password_reset/',
                    auth_view.PasswordResetView.as_view(
                    template_name='resetPassword.html'
                    ),
                    name='password_reset'
            ),
            path('reset/<uidb64>/<token>//',
                 auth_view.PasswordResetView.as_view(
                    template_name='registration/password_reset_confirm.html'
                    ), name='password_reset'),
            path('reset/<uidb64>/<token>/',
                 auth_view.PasswordResetConfirmView.as_view(
                    template_name='registration/password_reset_confirm.html'
                    ), name='password_reset_confirm'),
            path('password-reset/done/',
                 auth_view.PasswordResetDoneView.as_view(
                    template_name='registration/password_reset_done.html'
                    ), name='password_reset_done'),
        ])),
]

# urlpatterns += [
#     path('', views.flatpage, {'url': '/author/'}, name='about_author'),
#     path('', views.flatpage, {'url': '/tech/'}, name='about_tech'),
#
# ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)