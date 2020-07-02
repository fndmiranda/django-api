import factory
from datetime import timedelta
from django.utils import timezone
from faker import Factory
from core import settings
from user.factories import UserFactory
from oauth2_provider.models import (
    get_application_model,
    get_access_token_model,
    generate_client_id,
    generate_client_secret,
)
from oauthlib.common import generate_token

faker = Factory.create()


class ApplicationFactory(factory.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    authorization_grant_type = get_application_model().GRANT_PASSWORD
    name = settings.APP_NAME
    client_id = factory.Sequence(lambda n: '{}{}'.format(generate_client_id(), n))
    client_secret = generate_client_secret()
    client_type = get_application_model().CLIENT_CONFIDENTIAL
    skip_authorization = True
    redirect_uris = 'http://localhost'

    class Meta:
        model = get_application_model()


class AccessTokenFactory(factory.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    application = factory.SubFactory(ApplicationFactory)
    token = factory.Sequence(lambda n: '{}{}'.format(generate_token(), n))
    expires = timezone.now() + timedelta(days=1)
    scope = 'read write groups'

    class Meta:
        model = get_access_token_model()
