from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.utils.functional import lazy
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

mark_safe_lazy = lazy(mark_safe, str)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    # groups = serializers.HyperlinkedRelatedField(many=True, view_name='group-detail', read_only=True)
    first_name = serializers.CharField(required=True, max_length=30, help_text=_("The first name of the user."))
    last_name = serializers.CharField(required=True, max_length=150, help_text=_("The last name of the user."))
    email = serializers.EmailField(
        required=True,
        max_length=254,
        help_text=_("The email of the user."),
        validators=[UniqueValidator(queryset=get_user_model().objects.all())],
   )
    password = serializers.CharField(
        required=True,
        max_length=30,
        help_text=_("The password of the user."),
        write_only=True
    )
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

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = '__all__'
        # fields = (
        #     'url', 'id', 'first_name', 'last_name', 'email', 'is_active',
        #     'is_staff', 'is_superuser', 'last_login', 'date_joined', 'password'
        # )


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.CharField(required=True, max_length=80, help_text=_("The name of the group."))

    class Meta:
        model = Group
        fields = ('url', 'id', 'name')
