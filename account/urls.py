from django.conf.urls import url
from .views import AccountViewSet, PasswordResetViewSet

app_name = 'account'

account_list = AccountViewSet.as_view({
    'get': 'retrieve',
    'post': 'create',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})

password_reset_list = PasswordResetViewSet.as_view({
    'post': 'create',
    'put': 'update',
})

urlpatterns = [
    url(r'accounts', account_list, name='account-list'),
    url(r'password_resets', password_reset_list, name='password-reset-list'),
]
