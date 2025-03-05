from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = "Добавление пользователей в группу Менеджеры"

    def add_arguments(self, parser):
        parser.add_argument("emails", nargs="+", type=str, help="Email пользователей для добавления в группу")

    def handle(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name="Менеджеры")
        emails = kwargs["emails"]

        for email in emails:
            try:
                user = User.objects.get(email=email)
                user.groups.add(group)
                print(f"Пользователь {email} добавлен в группу Менеджеры.")
            except User.DoesNotExist:
                print(f"Пользователь {email} не найден.")

