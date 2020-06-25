import binascii
import os
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class PasswordResetToken(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='password_reset_tokens',
        on_delete=models.CASCADE,
        verbose_name=_("owner")
    )
    token = models.CharField(
        max_length=64,
        primary_key=True,
        verbose_name=_("token")
    )
    ip_address = models.GenericIPAddressField(
        default='127.0.0.1',
        verbose_name=_("ip address")
    )
    user_agent = models.CharField(
        max_length=256,
        verbose_name=_("user agent")
    )
    created = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def generate_token():
        """ Generate a token using os.urandom and binascii.hexlify """
        return binascii.hexlify(os.urandom(32)).decode()

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.generate_token()
        return super(PasswordResetToken, self).save(*args, **kwargs)
