import smtplib
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from config import settings
from mailing.forms import MessageForm, NewsletterForm, RecipientForm
from mailing.models import EmailAttempt, Message, Newsletter, Recipient
from users.models import User


class IndexView(TemplateView):

    template_name = "mailing/index.html"

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            context = super().get_context_data(**kwargs)
            user = self.request.user

            if user.groups.filter(name="Manager").exists():
                context["total_newsletters"] = Newsletter.objects.count()
                context["active_newsletters"] = Newsletter.objects.filter(status="started").count()
                context["unique_recipients"] = Recipient.objects.distinct().count()
            else:
                user_newsletters = Newsletter.objects.filter(owner=user)
                context["total_newsletters"] = user_newsletters.count()
                context["active_newsletters"] = user_newsletters.filter(status="started").count()
                context["unique_recipients"] = (
                    Recipient.objects.filter(mailing__in=user_newsletters).distinct().count()
                )

            return context


class RecipientListView(LoginRequiredMixin, ListView):
    model = Recipient

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Manager").exists():
            return Recipient.objects.all()
        return Recipient.objects.filter(owner=user)


class RecipientDetailView(LoginRequiredMixin, DetailView):
    model = Recipient


class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy("mailing:recipients_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipient
    fields = ["email", "full_name", "comment"]
    success_url = reverse_lazy("mailing:recipients_list")

    def dispatch(self, request, *args, **kwargs):
        object = super().get_object()
        if object.owner == self.request.user:
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied()


class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipient
    success_url = reverse_lazy("mailing:recipients_list")

    def dispatch(self, request, *args, **kwargs):
        object = super().get_object()
        if object.owner == self.request.user:
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied()


class MessageListView(LoginRequiredMixin, ListView):
    model = Message

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Manager").exists():
            return Message.objects.all()
        return Message.objects.filter(owner=user)


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:messages_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    fields = ["subject", "body"]
    success_url = reverse_lazy("mailing:messages_list")

    def dispatch(self, request, *args, **kwargs):
        object = super().get_object()
        if object.owner == self.request.user:
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied()


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy("mailing:messages_list")

    def dispatch(self, request, *args, **kwargs):
        obj = super().get_object()
        if obj.owner == self.request.user:
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied()


class NewsletterListView(LoginRequiredMixin, ListView):
    model = Newsletter

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Manager").exists():
            return Newsletter.objects.all()
        return Newsletter.objects.filter(owner=user)


class NewsletterDetailView(LoginRequiredMixin, DetailView):
    model = Newsletter

    def send_newsletter(self):
        recipients = self.object.recipients.all()
        success_count = 0
        failure_count = 0
        for recipient in recipients:
            try:
                self.object.start_time = datetime.now()
                self.object.status = "started"
                self.object.save()
                send_mail(
                    subject=self.object.message.subject,
                    message=self.object.message.body,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[recipient.email],
                )
                EmailAttempt.objects.create(
                    status="successful",
                    server_response=recipient.email + " Отправлено успешно",
                    newsletter=self.object,
                    owner=self.request.user,
                )
                success_count += 1
            except smtplib.SMTPException as e:
                failure_count += 1
                EmailAttempt.objects.create(
                    status="unsuccessful",
                    server_response=str(e),
                    newsletter=self.object,
                    fail_silently=False,
                    owner=self.request.user,
                )

        if success_count > 0 and failure_count == 0:
            self.object.status = "completed"
            messages.success(self.request, "Все письма отправлены успешно.")
        else:
            self.object.status = "started"
            messages.warning(self.request, f"{failure_count} письм(о/а) не отправлено.")

        self.object.end_time = datetime.now()
        self.object.save()

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if "send_newsletter" in request.POST:
            try:
                self.send_newsletter()
            except Exception as e:
                messages.error(request, f"Произошла ошибка при отправке рассылки: {str(e)}")

        return redirect("mailing:newsletters_detail", pk=self.object.pk)


class NewsletterCreateView(LoginRequiredMixin, CreateView):
    model = Newsletter
    form_class = NewsletterForm
    success_url = reverse_lazy("mailing:newsletters_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class NewsletterUpdateView(LoginRequiredMixin, UpdateView):
    model = Newsletter
    form_class = NewsletterForm
    success_url = reverse_lazy("mailing:newsletters_list")

    def dispatch(self, request, *args, **kwargs):
        object = super().get_object()
        if object.owner == self.request.user:
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied()


class NewsletterDeleteView(LoginRequiredMixin, DeleteView):
    model = Newsletter
    success_url = reverse_lazy("mailing:newsletters_list")

    def dispatch(self, request, *args, **kwargs):
        object = super().get_object()
        if object.owner == self.request.user:
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied()


class EmailAttemptListView(LoginRequiredMixin, ListView):
    model = EmailAttempt

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Manager").exists():
            return EmailAttempt.objects.all()
        return EmailAttempt.objects.filter(owner=user.id)


class EmailStopView(LoginRequiredMixin, View):
    def post(self, request, pk):
        email = get_object_or_404(Newsletter, pk=pk)
        user = request.user
        manager = user.groups.filter(name="Manager").exists()
        if manager or user == email.owner:
            email.status = "completed"
            email.save()

            return redirect("mailing:newsletters_list")
        raise PermissionDenied()
