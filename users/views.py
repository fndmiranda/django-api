from rest_framework import viewsets
from users.serializers import UserSerializer, GroupSerializer
from rest_framework import permissions
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from oauth2_provider.contrib.rest_framework import IsAuthenticatedOrTokenHasScope


class UserViewSet(viewsets.ModelViewSet):
    """
    list:
    Return the list of users.

    read:
    Return the specific user.

    create:
    Create a new user instance.

    update:
    Update a user instance.

    partial_update:
    Partial update a user instance.

    delete:
    Delete a user instance.
    """
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticatedOrTokenHasScope, permissions.DjangoModelPermissions,)
    required_scopes = ['read']

    # def perform_create(self, serializer):
    #     serializer.save(password=self.request.user)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['create', 'list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]


class GroupViewSet(viewsets.ModelViewSet):
    """
    list:
    Return the list of groups.

    read:
    Return the specific group.

    create:
    Create a new group instance.

    update:
    Update a group instance.

    partial_update:
    Partial update a group instance.

    delete:
    Delete a group instance.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticatedOrTokenHasScope, permissions.DjangoModelPermissions,)
    required_scopes = ['read']

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
