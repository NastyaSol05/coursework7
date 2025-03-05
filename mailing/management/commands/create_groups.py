from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = "Создание группы Менеджеры"

    def handle(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name="Менеджеры")

        if created:
            print("Группа Менеджеры успешно создана.")
        else:
            print("Группа Менеджеры уже существует.")