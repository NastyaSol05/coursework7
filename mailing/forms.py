from django.forms import BooleanField, ModelForm
from mailing.models import Newsletter, Message


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
        exclude = ("start_time", "end_time", "status")

class MessageForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Message
        fields = "__all__"