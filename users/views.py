import secrets

import six
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import CreateView, ListView

from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm
from users.models import User


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}/"
        send_mail(
            subject="Подтверждение почты",
            message=f"Для подтверждения вашей почты перейдите по ссылке: {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


class UserListView(LoginRequiredMixin, ListView):
    model = User


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


class BlockUserView(LoginRequiredMixin):
    def block_user(request, user_id):
        user = User.objects.get(id=user_id)
        user.is_active = not user.is_active
        user.save()
        return redirect(reverse("users:user_list"))


# def confirm_email(request, uidb64, token):
#     try:
#         uid = urlsafe_base64_decode(uidb64).decode()
#         user = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None
#
#     if user is not None and default_token_generator.check_token(user, token):
#         user.is_active = True
#         user.save()
#         return redirect('email_confirmed')  # URL подтверждения
#     else:
#         return render(request, 'email_confirm_failed.html')
#
#
# def send_confirmation_email(user):
#     token = default_token_generator.make_token(user)
#     uid = urlsafe_base64_encode(six.text_type(user.pk).encode('utf-8'))
#     link = f"http://{self.request.get_host()}/users/email-confirm/{token}/"
#     link = f"http://yourdomain.com{reverse('confirm_email', kwargs={'uidb64': uid, 'token': token})}"
#     send_mail(
#         'Подтвердите ваш email',
#         f'Перейдите по ссылке для подтверждения: {link}',
#         'from@example.com',
#         [user.email],
#         fail_silently=False,
#     )
