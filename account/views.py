import logging
from datetime import timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from rest_framework.permissions import AllowAny
from django.conf import settings
from account import serializers
from account.models import PasswordResetToken
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from user.models import User

logger = logging.getLogger('account.views')


class AccountViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user account instances.

    create:
    Create a new account.

    retrieve:
    Return the current account.

    update:
    Update the current account.

    partial_update:
    Partial update the current account.

    destroy:
    Destroy the current account.
    """
    def get_object(self):
        """Get the object this request displays."""
        return self.request.user

    def get_permissions(self):
        """Instantiates and returns the list of permissions that this view requires."""
        if self.action == 'create':
            classes = [permissions.AllowAny]
        else:
            classes = [permissions.IsAuthenticated]
        return [permission() for permission in classes]

    def create(self, request, *args, **kwargs):
        logger.info('Starting create a account')
        response = super().create(request, *args, **kwargs)
        logger.info('Response create a account with user id: {} status code: {} response keys: {}'.format(
            response.data['id'], response.status_code, list(response.data.keys()))
        )
        return response

    def retrieve(self, request, *args, **kwargs):
        logger.info('Starting retrieve a account from user id: {}'.format(request.user.id))
        response = super().retrieve(request, *args, **kwargs)
        logger.info('Response retrieve a account from user id: {} with status code: {} response keys: {}'.format(
            response.data['id'], response.status_code, list(response.data.keys()))
        )
        return response

    def update(self, request, *args, **kwargs):
        action = 'partial update' if kwargs.get('partial', False) else 'update'
        logger.info('Starting {} a account from user id: {} with payload keys: {}'.format(
            action, request.user.id, list(request.data.keys())
        ))
        response = super().update(request, *args, **kwargs)
        logger.info('Response {} a account from user id: {} with status code: {} response keys: {}'.format(
            action, response.data['id'], response.status_code, list(response.data.keys())
        ))
        return response

    def destroy(self, request, *args, **kwargs):
        user_id = request.user.id
        logger.info('Starting destroy a account from user id: {}'.format(user_id))
        response = super().destroy(request, *args, **kwargs)
        logger.info('Response destroy a account from user id: {} with status code: {}'.format(
            user_id, response.status_code
        ))
        return response

    def get_serializer_class(self):
        """Return the class to use for the serializer."""
        if self.action == 'update':
            return serializers.AccountUpdateSerializer
        else:
            return serializers.AccountSerializer


class PasswordResetViewSet(viewsets.GenericViewSet):
    """
    A viewset for reset the password for a user account.

    create:
    Create a new password reset.

    update:
    Update the account password using a reset token.
    """
    permission_classes = [AllowAny]
    lookup_field = 'token'

    def get_queryset(self):
        return User.objects.all()

    def get_serializer_class(self):
        """Return the class to use for the serializer."""
        if self.action == 'create':
            return serializers.PasswordResetTokenSerializer
        elif self.action == 'update':
            return serializers.PasswordResetSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            # find a user by email address (case insensitive search)
            user = User.objects.filter(email__iexact=serializer.data['email']).get()
            if user.is_active and user.has_usable_password():
                expiry_time = timezone.now() - timedelta(hours=settings.API_PASSWORD_RESET_TOKEN_EXPIRY)

                try:
                    password_reset_token = user.password_reset_tokens.filter(created__gte=expiry_time).get()
                except ObjectDoesNotExist:
                    password_reset_token = PasswordResetToken.objects.create(
                        owner=user,
                        user_agent=request.META['HTTP_USER_AGENT'],
                        ip_address=request.META['REMOTE_ADDR']
                    )

                context = {
                    'request': request,
                    'settings': settings,
                    'user': user,
                    'password_reset_token': password_reset_token,
                }

                # Debug response with html
                # from django.shortcuts import render
                # return render(request, 'account/password_reset_token_mail.html', context)

                message = render_to_string('account/password_reset_token_mail.html', context)
                email_message = EmailMessage(
                    subject=_('Password reset'),
                    body=message,
                    from_email='from@example.com',
                    to=[user.email]
                )
                email_message.content_subtype = 'html'
                email_message.send(fail_silently=False)

        except ObjectDoesNotExist:
            return Response(data={'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            password_reset_token = PasswordResetToken.objects.filter(token=kwargs['token']).get()
            user = password_reset_token.owner

            if user.is_active and user.has_usable_password():
                user.set_password(serializer.data['password'])
                user.save()

                return Response(data={'detail': 'OK'}, status=status.HTTP_200_OK)
            else:
                return Response(data={'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        except ObjectDoesNotExist:
            return Response(data={'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
