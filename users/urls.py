from django.urls import path
from django.contrib.auth import views as auth_view

from .views import SignUp

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
]
