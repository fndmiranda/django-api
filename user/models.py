from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils.translation import gettext_lazy as _
from django.utils.functional import lazy
from django.utils.safestring import mark_safe

mark_safe_lazy = lazy(mark_safe, str)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, name, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, name=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, name, **extra_fields)

    def create_superuser(self, email, password, name, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, name, **extra_fields)


class User(AbstractBaseUser):
    email = models.EmailField(max_length=254, unique=True, verbose_name=_("email address"))
    name = models.CharField(max_length=180, blank=False, verbose_name=_("name"))
    date_joined = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=128, blank=False)
    language = models.CharField(
        max_length=5,
        verbose_name=_('language'),
        blank=False,
        choices=settings.LANGUAGES,
        default=settings.LANGUAGE_DEFAULT,
    )
    is_superuser = models.BooleanField(
        default=False,
        help_text='Designates that this user has all permissions without explicitly assigning them.',
        verbose_name='superuser status',
    )
    is_active = models.BooleanField(
        default=True, verbose_name='active', help_text=(
            'Designates whether this user should be treated as active. Unselect this instead of deleting '
            'accounts.'
        )
    )
    is_staff = models.BooleanField(
        default=False,
        help_text='Designates whether the user can log into this admin site.',
        verbose_name='staff status',
    )
    last_login = models.DateTimeField(auto_now_add=True)
    date_joined = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-date_joined']

    def __str__(self):
        return self.name

    def send_email(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
