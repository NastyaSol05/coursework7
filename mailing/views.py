from django.forms import inlineformset_factory
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from mailing.forms import NewsletterForm, MessageForm
from mailing.models import Recipient, Message, Newsletter


class RecipientListView(ListView):
    model = Recipient

    def get_queryset(self):
        return Recipient.objects.all()

class RecipientDetailView(DetailView):
    model = Recipient


class RecipientCreateView(CreateView):
    model = Recipient

class RecipientUpdateView(UpdateView):
    model = Recipient
    fields = ["email", "full_name", "comment"]

class RecipientDeleteView(DeleteView):
    model = Recipient

class MessageListView(ListView):
    model = Message

    def get_queryset(self):
        return Message.objects.all()

class MessageDetailView(DetailView):
    model = Message


class MessageCreateView(CreateView):
    model = Message


class MessageUpdateView(UpdateView):
    model = Message
    fields = ["subject", "body"]


class MessageDeleteView(DeleteView):
    model = Message

class NewsletterListView(ListView):
    model = Newsletter

    def get_queryset(self):
        return Newsletter.objects.all()


class NewsletterDetailView(DetailView):
    model = Newsletter


class NewsletterCreateView(CreateView):
    model = Newsletter
    form_class = NewsletterForm
    success_url = reverse_lazy("mailing:newsletter_list")



class NewsletterUpdateView(UpdateView):
    model = Newsletter
    form_class = NewsletterForm
    success_url = reverse_lazy("mailing:newsletter_list")



class NewsletterDeleteView(DeleteView):
    model = Newsletter




