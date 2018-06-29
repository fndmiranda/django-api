from rest_framework import serializers
from django.contrib.auth.models import User, Group
from django.utils.functional import lazy
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

mark_safe_lazy = lazy(mark_safe, str)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    groups = serializers.HyperlinkedRelatedField(many=True, view_name='group-detail', read_only=True)
    first_name = serializers.CharField(required=True, max_length=30, help_text=_("The first name of the user."))
    last_name = serializers.CharField(required=True, max_length=150, help_text=_("The last name of the user."))
    email = serializers.EmailField(required=True, max_length=254, help_text=_("The email of the user."))
    is_active = serializers.BooleanField(required=False, help_text=mark_safe_lazy(_(
        """
        If user is active, default is <code>True</code>.
        """
    )))
    is_staff = serializers.BooleanField(required=False, help_text=mark_safe_lazy(_(
        """
        If user is staff, default is <code>True</code>.
        """
    )))
    is_superuser = serializers.BooleanField(required=False, help_text=mark_safe_lazy(_(
        """
        If user is superuser, default is <code>False</code>.
        """
    )))

    class Meta:
        model = User
        fields = (
            'url', 'id', 'first_name', 'last_name', 'email', 'is_active',
            'is_staff', 'is_superuser', 'last_login', 'date_joined', 'groups'
        )


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.CharField(required=True, max_length=80, help_text=_("The name of the group."))

    class Meta:
        model = Group
        fields = ('url', 'id', 'name')
