from django.contrib.auth import views as auth_view
from django.urls import include, path
from django.contrib.auth import views as auth_views

from .views import SignUp

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
]


urlpatterns += [
    path('auth/', include([
            path('login/', auth_view.LoginView.as_view(
                template_name='registration/reg.html'), name='login'
            ),
            path('logout/', auth_view.LogoutView.as_view(
                template_name='registration/logged_out.html'), name='logout'
            ),
            path('password-change/', auth_view.PasswordChangeView.as_view(
                template_name='registration/password_change_form.html'
                ), name='password_change'
            ),
            path('password-reset/', auth_views.PasswordResetView.as_view(
                template_name='registration/password_reset_form.html'
                ),
                name='password_reset'
            ),
            path(
                'password-reset-done/',
                auth_views.PasswordResetDoneView.as_view(
                    template_name='registration/password_reset_done.html'
                ),
                name='password_reset_done'
            ),
            path(
                'password-reset-confirm/',
                auth_views.PasswordResetConfirmView.as_view(
                    template_name='registration/password_reset_confirm.html'
                ),
                name='password_reset_confirm'
            ),
        ])),
]
