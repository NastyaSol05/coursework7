from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=50, unique=False, blank=True, null=True, default="")
    email = models.EmailField(unique=True, verbose_name="Email")

    phone = models.CharField(
        max_length=35, verbose_name="Phone", blank=True, null=True, help_text="Введите номер телефона"
    )
    country = models.CharField(max_length=50, verbose_name="Страна", blank=True, null=True, help_text="Введите страну")
    avatar = models.ImageField(
        upload_to="users/avatars/", verbose_name="Avatar", blank=True, null=True, help_text="Загрузите свой аватар"
    )

    token = models.CharField(max_length=100, verbose_name="Token", blank=True, null=True)

    groups = models.ManyToManyField("auth.Group", related_name="custom_user_set", blank=True, verbose_name="Группы")

    user_permissions = models.ManyToManyField(
        "auth.Permission", related_name="custom_user_permissions_set", blank=True, verbose_name="Разрешения"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

        permissions = [("can_block_user", "Can block users")]

    def __str__(self):
        return self.email
