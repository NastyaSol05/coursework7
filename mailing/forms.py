from django.forms import BooleanField, ModelForm

from mailing.models import Message, Newsletter, Recipient


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fild_name, fild in self.fields.items():
            if isinstance(fild, BooleanField):
                fild.widget.attrs["class"] = "form-check-input"
            else:
                fild.widget.attrs["class"] = "form-control"


class NewsletterForm(StyleFormMixin, ModelForm):

    class Meta:
        model = Newsletter
        exclude = ("start_time", "end_time", "status", "owner")


class MessageForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Message
        exclude = ("owner",)


class RecipientForm(StyleFormMixin, ModelForm):

    class Meta:
        model = Recipient
        exclude = ("owner",)


class RecipientModeratorForm(StyleFormMixin, ModelForm):

    class Meta:
        model = Recipient
        fields = "__all__"


class MessageModeratorForm(StyleFormMixin, ModelForm):

    class Meta:
        model = Message
        fields = "__all__"


class NewsletterModeratorForm(StyleFormMixin, ModelForm):

    class Meta:
        model = Newsletter
        fields = "__all__"
