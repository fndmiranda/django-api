from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
from django.utils.functional import lazy
from django.utils.safestring import mark_safe
from django.conf import settings
from django.utils.translation import gettext_lazy as _

mark_safe_lazy = lazy(mark_safe, str)


class PasswordResetTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, help_text=_("The email to get password reset token."))


class PasswordResetSerializer(serializers.Serializer):
    token = serializers.CharField(required=True, help_text=_("The password reset token."))
    password = serializers.CharField(required=True, help_text=_("The new password."))


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    first_name = serializers.CharField(required=True, max_length=30, help_text=_("The first name of the account."))
    last_name = serializers.CharField(required=True, max_length=150, help_text=_("The last name of the account."))
    email = serializers.EmailField(
        required=True,
        max_length=254,
        help_text=_("The email of the user."),
        validators=[UniqueValidator(queryset=get_user_model().objects.all())],
    )
    language = serializers.ChoiceField(required=False, choices=settings.LANGUAGES, help_text=mark_safe_lazy(
        "%s: [%s] %s %s" % (
            _('	The language of the account, options: '),
            ', '.join("{!s}".format(key, val) for (key, val) in settings.LANGUAGES),
            _('default is'),
            "<code>%s</code>" % settings.LANGUAGE_DEFAULT
        )
    ))
    is_staff = serializers.BooleanField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    password = serializers.CharField(
        required=True,
        max_length=30,
        help_text=_("The password of the user."),
        write_only=True
    )

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        if 'password' in validated_data:
            user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = [
            'id', 'first_name', 'last_name', 'email', 'language', 'is_superuser',
            'is_active', 'is_staff', 'password', 'date_joined', 'updated'
        ]


class AccountChangeSerializer(AccountSerializer):
    password = serializers.CharField(
        required=False,
        max_length=30,
        help_text=_("The password of the account."),
        write_only=True,
    )
