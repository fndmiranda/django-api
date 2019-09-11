from datetime import timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from accounts import serializers
from accounts.serializers import AccountSerializer, PasswordResetTokenSerializer, PasswordResetSerializer
from accounts.models import PasswordResetToken
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _


class AccountViewSet(viewsets.ModelViewSet):
    """
    create:
    Create a new account instance.

    show:
    Return the current account instance.

    change:
    Update the current account instance.

    password_reset_token:
    Get one password reset token from a account.

    password_reset:
    Change the password from a account with one password reset token.

    account_delete:
    Destroy the current account instance.

    list:
    Action disabled.

    read:
    Action disabled.

    update:
    Action disabled.

    partial_update:
    Action disabled.

    delete:
    Action disabled.
    """
    queryset = get_user_model().objects.all()
    serializer_class = AccountSerializer

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.action == 'password_reset_token':
            return serializers.PasswordResetTokenSerializer
        elif self.action == 'password_reset':
            return serializers.PasswordResetSerializer
        elif self.action == 'change':
            return serializers.AccountChangeSerializer
        return serializers.AccountSerializer

    def list(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(methods=['get'], detail=False)
    def show(self, request):
        serializer = AccountSerializer(self.get_object(), context={'request': request})
        return Response(data=serializer.data)

    @action(methods=['put'], detail=False)
    def change(self, request):
        serializer = serializers.AccountChangeSerializer(self.get_object(), context={'request': request}, data=request.data)
        if serializer.is_valid():
            self.perform_update(serializer)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data)

    @action(methods=['post'], detail=False)
    def password_reset_token(self, request):
        serializer = PasswordResetTokenSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # find a user by email address (case insensitive search)
                user = self.queryset.filter(email__iexact=serializer.data['email']).get()
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
                    return render(request, 'accounts/password_reset_token_mail.html', context)

                    # message = render_to_string('accounts/password_reset_token_mail.html', context)
                    # email_message = EmailMessage(
                    #     subject=_('Password reset'),
                    #     body=message,
                    #     from_email='from@example.com',
                    #     to=[user.email]
                    # )
                    # email_message.content_subtype = 'html'
                    # email_message.send(fail_silently=False)

            except ObjectDoesNotExist:
                pass
            return Response(data={'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def password_reset(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            try:
                password_reset_token = PasswordResetToken.objects.filter(token=serializer.data['token']).get()
                user = password_reset_token.owner

                if user.is_active and user.has_usable_password():
                    user.set_password(serializer.data['password'])
                    user.save()

                    return Response(data={'detail': 'OK'}, status=status.HTTP_200_OK)
                else:
                    return Response(data={'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
            except ObjectDoesNotExist:
                return Response(data={'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['password_reset_token', 'password_reset']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(methods=['delete'], detail=False)
    def account_delete(self, request):
        try:
            self.get_object().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_400_BAD_REQUEST)

