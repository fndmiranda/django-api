from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from catalog.models import Category
from catalog.factories import CategoryFactory, ProductFactory
from user.factories import UserFactory
from base.factories import AccessTokenFactory


class CategoryTests(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.keys = ['id', 'title', 'slug']
        self.headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + AccessTokenFactory(user=self.user).token,
        }

    def test_create_category(self):
        """
        Ensure we can create a new category object.
        """
        url = reverse('catalog:category-list')
        data = {key: CategoryFactory.build().__dict__[key] for key in ['title', 'slug']}

        response = self.client.post(url, data=data, format='json', **self.headers)

        instance = Category.objects.get(slug=data['slug'])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(instance.title, data['title'])

    def test_retrieve_category(self):
        """
        Ensure we can retrieve a category object.
        """
        instance = CategoryFactory.create()
        url = reverse('catalog:category-detail', kwargs={'pk': instance.id})

        response = self.client.get(url, format='json')

        for key in self.keys:
            self.assertIn(key, response.data)

        for key in self.keys:
            self.assertEqual(response.data[key], getattr(instance, key))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_category(self):
        """
        Ensure we can update a category object.
        """
        instance = CategoryFactory.create()
        data = {key: CategoryFactory.build().__dict__[key] for key in ['title', 'slug']}
        url = reverse('catalog:category-detail', kwargs={'pk': instance.id})

        response = self.client.put(url, data=data, format='json', **self.headers)

        for key in self.keys:
            self.assertIn(key, response.data)

        for key in data.keys():
            self.assertEqual(response.data[key], data[key])

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_category(self):
        """
        Ensure we can delete a category object.
        """
        instance = CategoryFactory.create()
        url = reverse('catalog:category-detail', kwargs={'pk': instance.id})

        response = self.client.delete(url, format='json', **self.headers)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ProductTests(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.keys = ['id', 'title', 'slug', 'description', 'brand', 'is_active', 'ordering']
        self.headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + AccessTokenFactory(user=self.user).token,
        }

    def test_create_product(self):
        """
        Ensure we can create a new product object.
        """
        url = reverse('catalog:product-list')
        data = {key: ProductFactory.build().__dict__[key] for key in [
            'title', 'slug', 'description', 'brand', 'is_active', 'ordering'
        ]}

        print('//////////////////')
        print('test1 - {}'.format(data))
        print('//////////////////')

        # response = self.client.post(url, data=data, format='json', **self.headers)
        #
        # instance = Category.objects.get(slug=data['slug'])
        #
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # self.assertEqual(instance.title, data['title'])

    def test_retrieve_category(self):
        """
        Ensure we can retrieve a category object.
        """
        instance = CategoryFactory.create()
        url = reverse('catalog:category-detail', kwargs={'pk': instance.id})

        response = self.client.get(url, format='json')

        for key in self.keys:
            self.assertIn(key, response.data)

        for key in self.keys:
            self.assertEqual(response.data[key], getattr(instance, key))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_category(self):
        """
        Ensure we can update a category object.
        """
        instance = CategoryFactory.create()
        data = {key: CategoryFactory.build().__dict__[key] for key in ['title', 'slug']}
        url = reverse('catalog:category-detail', kwargs={'pk': instance.id})

        response = self.client.put(url, data=data, format='json', **self.headers)

        for key in self.keys:
            self.assertIn(key, response.data)

        for key in data.keys():
            self.assertEqual(response.data[key], data[key])

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_category(self):
        """
        Ensure we can delete a category object.
        """
        instance = CategoryFactory.create()
        url = reverse('catalog:category-detail', kwargs={'pk': instance.id})

        response = self.client.delete(url, format='json', **self.headers)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)