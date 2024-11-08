# users/urls.py
from django.urls import path
from .views import (
    RegisterUserView,
    UserProfileView,
    UserListView,
    UserUpdateView,
    LoginView,
)

urlpatterns = [
    path("register/", RegisterUserView.as_view(), name="register"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("users/", UserListView.as_view(), name="user_list"),  # Admin
    path("users/<int:pk>/", UserUpdateView.as_view(), name="user_update"),  # Admin
    path("login/", LoginView.as_view(), name="login"),
]
