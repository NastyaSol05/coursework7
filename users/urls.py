from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.urls import include, path, reverse_lazy
from mypy.nodes import Block

from users.apps import UsersConfig
from users.views import BlockUserView, UserCreateView, UserListView, email_verification

app_name = UsersConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", UserCreateView.as_view(), name="register"),
    path("email-confirm/<str:token>/", email_verification, name="email-confirm"),
    path(
        "password_reset/",
        PasswordResetView.as_view(
            email_template_name="password_reset_email.html",
            success_url=reverse_lazy("users:password_reset_done"),
        ),
        name="password_reset",
    ),
    path("password_reset/done/", PasswordResetDoneView.as_view(), name="password_reset_done"),
    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(success_url=reverse_lazy("users:password_reset_complete")),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path("user_list/", UserListView.as_view(template_name="user_list.html"), name="user_list"),
    path("block_user/<int:user_id>/", BlockUserView.block_user, name="block_user"),
]
