from django.conf.urls.static import static
from django.urls import path
from django.views.decorators.cache import cache_page


from config import settings
from mailing.apps import MailingConfig
from mailing.views import NewsletterListView, NewsletterDetailView, NewsletterCreateView

app_name = MailingConfig.name


urlpatterns = [
    path("", NewsletterListView.as_view(), name="newsletters_list"),
    path("mailing/<int:pk>/", cache_page(60)(NewsletterDetailView.as_view()), name="newsletters_detail"),
    path("mailing/create", NewsletterCreateView.as_view(), name="newsletters_create"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
