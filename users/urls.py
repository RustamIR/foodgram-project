from django.contrib.auth import views as auth_view
from django.urls import include, path

from .views import SignUp

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
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
            path('reset/<uidb64>/<token>/',
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
