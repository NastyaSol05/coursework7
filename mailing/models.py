from django.core.cache import cache
from django.db import models
from django.utils import timezone

from users.models import User


class Recipient(models.Model):
    email = models.EmailField(unique=True, verbose_name="Почта", help_text="Введите адрес почты:")
    full_name = models.CharField(max_length=255, verbose_name="ФИО")
    comment = models.TextField(null=True, blank=True, verbose_name="Комментарий")

    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"

    def __str__(self):
        return self.email


class Message(models.Model):
    subject = models.CharField(max_length=255, verbose_name="Тема письма")
    body = models.TextField(verbose_name="Тело письма")

    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return self.subject


class Newsletter(models.Model):

    STATUS_CHOICES = [
        ("created", "Создана"),
        ("started", "Запущена"),
        ("completed", "Завершена"),
    ]

    start_time = models.DateTimeField(null=True, blank=True, verbose_name="Дата и время первой отправки")
    end_time = models.DateTimeField(null=True, blank=True, verbose_name="Дата и время окончания отправки")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="created", verbose_name="Статус рассылки")
    message = models.ForeignKey("Message", on_delete=models.CASCADE)
    recipients = models.ManyToManyField(Recipient, related_name="mailing", verbose_name="Получатели")

    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        permissions = [
            ("can_view_detail_newsletter", "Can view detail newsletter"),
            ("can_delete_newsletter", "Can view detail newsletter"),
        ]

    def __str__(self):
        return f"Рассылка {self.status} с темой: {self.message.subject}"


class EmailAttempt(models.Model):
    STATUS_CHOICES = [
        ("successful", "Успешно"),
        ("unsuccessful", "Не успешно"),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    attempt_time = models.DateTimeField(default=timezone.now, verbose_name="Дата и время попытки")
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, verbose_name="Статус")
    server_response = models.TextField(verbose_name="Ответ почтового сервера", blank=True)
    newsletter = models.ForeignKey(
        Newsletter, on_delete=models.CASCADE, related_name="email_attempts", verbose_name="Рассылка"
    )

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылки"

    def __str__(self):
        return f"Попытка рассылки {self.newsletter} - {self.status}"
