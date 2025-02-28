from django.contrib import admin

from mailing.models import EmailAttempt, Message, Newsletter, Recipient


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ("email", "full_name")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("subject", "body")


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ("id", "start_time", "end_time", "status", "message", "get_recipients")

    def get_recipients(self, obj):
        return ", ".join([r.email for r in obj.recipients.all()])


@admin.register(EmailAttempt)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("attempt_time", "status", "server_response", "newsletter")
