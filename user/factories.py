import factory
from faker import Factory
from user.models import User
from django.contrib.auth.hashers import make_password

faker = Factory.create()


class UserFactory(factory.DjangoModelFactory):
    email = factory.Sequence(lambda n: 'email{}@factory.com'.format(n))
    name = faker.name()
    password = make_password('secret')

    class Meta:
        model = User
