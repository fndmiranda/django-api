from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from user.models import User
from user.factories import UserFactory
from base.factories import AccessTokenFactory, ApplicationFactory
from oauth2_provider.models import get_application_model


class AccountTests(APITestCase):
    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('account:account-list')
        data = {'name': 'Fernando Miranda', 'email': 'fndmiranda@gmail.com', 'password': 'secret'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().name, 'Fernando Miranda')
        self.assertEqual(User.objects.get().email, 'fndmiranda@gmail.com')

    def test_retrieve_account(self):
        """
        Ensure we can retrieve a current account object.
        """
        user = UserFactory()
        url = reverse('account:account-list')
        access_token = AccessTokenFactory(user=user)
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + access_token.token,
        }
        response = self.client.get(url, format='json', **headers)

        self.assertEqual(user.email, response.data.get('email'))
        self.assertEqual(user.name, response.data.get('name'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_account(self):
        """
        Ensure we can update the current account object.
        """
        user = UserFactory()
        data = {
            'name': 'Name testing update',
            'email': 'update@testing.com',
            'password': 'secret_updated',
        }

        partial_data = {
            'name': 'Name testing partial update',
            'email': 'partial_update@testing.com',
            'password': 'secret_partial_updated',
        }

        url = reverse('account:account-list')
        access_token = AccessTokenFactory(user=user)
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + access_token.token,
        }
        response_put = self.client.put(url, data=data, format='json', **headers)
        self.assertTrue(User.objects.filter(name=data['name'], email=data['email']).exists())
        for key in ['name', 'email']:
            self.assertEqual(data[key], response_put.data[key])

        response_patch = self.client.patch(url, data=partial_data, format='json', **headers)
        self.assertTrue(User.objects.filter(name=partial_data['name'], email=partial_data['email']).exists())
        for key in ['name', 'email']:
            self.assertEqual(partial_data[key], response_patch.data[key])

        self.assertEqual(response_put.status_code, status.HTTP_200_OK)
        self.assertEqual(response_patch.status_code, status.HTTP_200_OK)

    def test_destroy_account(self):
        """
        Ensure we can destroy the current account object.
        """
        user = UserFactory()

        url = reverse('account:account-list')
        access_token = AccessTokenFactory(user=user)
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + access_token.token,
        }
        response = self.client.delete(url, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_token(self):
        """
        Ensure we can create a account token object.
        """
        application = ApplicationFactory()
        user = UserFactory(email='email.testing@testing.com')

        data = {
            'grant_type': get_application_model().GRANT_PASSWORD,
            'username': user.email,
            'password': 'secret',
            'client_id': application.client_id,
            'client_secret': application.client_secret,
        }

        url = reverse('oauth2_provider:token')
        response = self.client.post(url, data=data)

        self.assertIn('access_token', response.json())
        self.assertIn('expires_in', response.json())
        self.assertIn('token_type', response.json())
        self.assertIn('scope', response.json())
        self.assertIn('refresh_token', response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
