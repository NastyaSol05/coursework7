from datetime import datetime

from django.db import models


class Recipient(models.Model):
    email = models.EmailField(unique=True, verbose_name='Почта', help_text='Введите адрес почты:')
    full_name = models.CharField(max_length=255, verbose_name='ФИО')
    comment = models.TextField(null=True, blank=True, verbose_name='Комментарий')

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"

    def __str__(self):
        return self.email

class Message(models.Model):
    subject = models.CharField(max_length=255, verbose_name='Тема письма')
    body = models.TextField(verbose_name='Тело письма')

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return self.subject


class Newsletter(models.Model):
    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('completed', 'Завершена'),
    ]

    start_time = models.DateTimeField(verbose_name='Дата и время первой отправки')
    end_time = models.DateTimeField(verbose_name='Дата и время окончания отправки')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='created', verbose_name='Статус рассылки')
    message = models.ForeignKey('Message', on_delete=models.CASCADE)
    recipients = models.ManyToManyField(Recipient, related_name="mailing", verbose_name="Получатели")

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"

    def __str__(self):
        return f"Рассылка {self.status} с темой: {self.message.subject}"


class SendingAttempt(models.Model):
    STATUS_CHOICES = [
        ('successful', 'Успешно'),
        ('unsuccessful', 'Не успешно'),
    ]

    attempt_time = models.DateTimeField()
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, verbose_name='Статус')
    server_response = models.TextField(null=True, blank=True, verbose_name='Ответ сервера')
    newsletter = models.ForeignKey('Newsletter', on_delete=models.CASCADE, verbose_name='Рассылка')

    class Meta:
        verbose_name = "Попытка отправки"
        verbose_name_plural = "Попытки отправки"

    def __str__(self):
        return f"Попытка {self.status} для рассылки {self.newsletter.id} в {self.attempt_time}"
