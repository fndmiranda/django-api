from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from core import settings
from oauth2_provider.models import get_application_model, generate_client_id, generate_client_secret
from user.models import User


class Command(BaseCommand):
    help = 'Create a OAuth2 application on the Authorization server.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--name',
            default=settings.APP_NAME,
            type=str,
            help='The name this application',
        )

        parser.add_argument(
            '--user',
            default=None,
            type=int,
            help="The redirect URIs, this must be a space separated string e.g 'URI1 URI2'",
        )

        parser.add_argument(
            '--client_id',
            default=generate_client_id(),
            type=str,
            help='The client identifier',
        )

        parser.add_argument(
            '--client_secret',
            default=generate_client_secret(),
            type=str,
            help='The client confidential secret',
        )

        parser.add_argument(
            '--redirect_uris',
            default='',
            type=str,
            help='The list of allowed redirect uri. The string consists of valid URLs separated by space',
        )

        parser.add_argument(
            '--client_type',
            choices=[get_application_model().CLIENT_CONFIDENTIAL, get_application_model().CLIENT_PUBLIC],
            default=get_application_model().CLIENT_CONFIDENTIAL,
            type=str,
            help='Client type, can be confidential or public',
        )

        parser.add_argument(
            '--grant_type',
            choices=[
                get_application_model().GRANT_AUTHORIZATION_CODE,
                get_application_model().GRANT_IMPLICIT,
                get_application_model().GRANT_PASSWORD,
                get_application_model().GRANT_CLIENT_CREDENTIALS,
            ],
            default=get_application_model().GRANT_PASSWORD,
            type=str,
            help='Authorization flows available to the Application',
        )

        parser.add_argument(
            '--skip',
            default=False,
            action='store_true',
            help='Skip authorization',
        )

    def handle(self, *args, **options):
        data = {
            'name': options['name'],
            'user_id': options['user'],
            'client_id': options['client_id'],
            'redirect_uris': options['redirect_uris'],
            'client_secret': options['client_secret'],
            'client_type': options['client_type'],
            'authorization_grant_type': options['grant_type'],
            'skip_authorization': options['skip'],
        }

        try:
            if options['user'] is not None:
                user = User.objects.get(pk=options['user'])
                data.update({
                    'user_id': user.id
                })

            obj = get_application_model()(**data)
            obj.clean()
            obj.save()

            self.stdout.write(self.style.SUCCESS('New OAuth2 application created successfully!'))
            self.stdout.write('{} {}'.format(self.style.SUCCESS('Application name:'), self.style.WARNING(obj.name)))
            self.stdout.write('{} {}'.format(self.style.SUCCESS('Client ID:'), self.style.WARNING(obj.client_id)))
            self.stdout.write('{} {}'.format(self.style.SUCCESS('Client secret:'),
                                             self.style.WARNING(obj.client_secret)))
            self.stdout.write('{} {}'.format(self.style.SUCCESS('Client type:'), self.style.WARNING(obj.client_type)))
            self.stdout.write('{} {}'.format(self.style.SUCCESS('Grant type:'),
                                             self.style.WARNING(obj.authorization_grant_type)))
        except ValidationError as e:
            self.stdout.write(self.style.ERROR(e.message))
        except ObjectDoesNotExist as e:
            self.stdout.write(self.style.ERROR(e))
        except Exception as e:
            self.stdout.write(self.style.ERROR(e))
