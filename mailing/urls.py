from django.conf.urls.static import static
from django.urls import path
from django.views.decorators.cache import cache_page

from config import settings
from mailing.apps import MailingConfig
from mailing.models import EmailAttempt
from mailing.views import (
    EmailAttemptListView,
    IndexView,
    MessageCreateView,
    MessageDeleteView,
    MessageDetailView,
    MessageListView,
    MessageUpdateView,
    NewsletterCreateView,
    NewsletterDeleteView,
    NewsletterDetailView,
    NewsletterListView,
    NewsletterUpdateView,
    RecipientCreateView,
    RecipientDeleteView,
    RecipientDetailView,
    RecipientListView,
    RecipientUpdateView,
)

app_name = MailingConfig.name


urlpatterns = [
    path("", IndexView.as_view(), name=""),
    path("index", IndexView.as_view(), name="index"),
    path("newsletters/", NewsletterListView.as_view(), name="newsletters_list"),
    path("newsletters/<int:pk>/", cache_page(60)(NewsletterDetailView.as_view()), name="newsletters_detail"),
    path("newsletters/create/", NewsletterCreateView.as_view(), name="newsletters_create"),
    path("newsletters/<int:pk>/update/", NewsletterUpdateView.as_view(), name="newsletters_update"),
    path("newsletters/<int:pk>/delete/", NewsletterDeleteView.as_view(), name="newsletters_delete"),
    path("messages/", MessageListView.as_view(), name="messages_list"),
    path("messages/<int:pk>/", cache_page(60)(MessageDetailView.as_view()), name="messages_detail"),
    path("messages/create/", MessageCreateView.as_view(), name="messages_create"),
    path("messages/<int:pk>/update/", MessageUpdateView.as_view(), name="messages_update"),
    path("messages/<int:pk>/delete/", MessageDeleteView.as_view(), name="messages_delete"),
    path("recipients/", RecipientListView.as_view(), name="recipients_list"),
    path("recipients/<int:pk>/", cache_page(60)(RecipientDetailView.as_view()), name="recipients_detail"),
    path("recipients/create/", RecipientCreateView.as_view(), name="recipients_create"),
    path("recipients/<int:pk>/update/", RecipientUpdateView.as_view(), name="recipients_update"),
    path("recipients/<int:pk>/delete/", RecipientDeleteView.as_view(), name="recipients_delete"),
    path("email_attempt_list", cache_page(5)(EmailAttemptListView.as_view()), name="email_attempt_list"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
