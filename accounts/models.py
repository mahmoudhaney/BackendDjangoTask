from django.db import models
from django.db.models import Q
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    """
    email_message = "http://127.0.0.1:8000{}?token={}".format(reverse('accounts:password_reset:reset-password-confirm'), reset_password_token.key)
    send_mail(
        "Reset Account Password",
        email_message,
        settings.EMAIL_HOST_USER,
        [reset_password_token.user.email],
    )

class User(AbstractUser):
    address = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=11, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['phone_number'], condition=Q(phone_number__isnull=False), name='unique_phone_number'),
        ]

    def __str__(self) -> str:
        return str(self.username)