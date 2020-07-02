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
        mock = {key: ProductFactory.build().__dict__[key] for key in [
            'title', 'slug', 'description', 'brand', 'is_active', 'ordering'
        ]}

        data = mock.copy()
        categories = [category.id for category in CategoryFactory.create_batch(5)]
        data.update({'categories': categories})

        response = self.client.post(url, data=data, format='json', **self.headers)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(sorted(categories), sorted([category['id'] for category in response.data['categories']]))
        for key in mock.keys():
            self.assertEqual(response.data[key], data[key])

    def test_retrieve_product(self):
        """
        Ensure we can retrieve a product object.
        """
        instance = ProductFactory.create(categories=CategoryFactory.create_batch(5))
        url = reverse('catalog:product-detail', kwargs={'pk': instance.id})

        response = self.client.get(url, format='json')

        self.assertEqual(len(response.data['categories']), instance.categories.count())

        for key in self.keys:
            self.assertIn(key, response.data)

        for key in self.keys:
            self.assertEqual(response.data[key], getattr(instance, key))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_product(self):
        """
        Ensure we can update a product object.
        """
        instance = ProductFactory.create(categories=CategoryFactory.create_batch(5))
        mock = {key: ProductFactory.build().__dict__[key] for key in [
            'title', 'slug', 'description', 'brand', 'is_active', 'ordering'
        ]}
        data = mock.copy()
        categories = [category.id for category in CategoryFactory.create_batch(5)]
        data.update({'categories': categories})

        url = reverse('catalog:product-detail', kwargs={'pk': instance.id})

        response = self.client.put(url, data=data, format='json', **self.headers)

        self.assertEqual(len(response.data['categories']), instance.categories.count())
        self.assertEqual(sorted(categories), sorted([category['id'] for category in response.data['categories']]))

        for key in self.keys:
            self.assertIn(key, response.data)

        for key in mock.keys():
            self.assertEqual(response.data[key], data[key])

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_product(self):
        """
        Ensure we can delete a product object.
        """
        instance = ProductFactory.create()
        url = reverse('catalog:product-detail', kwargs={'pk': instance.id})

        response = self.client.delete(url, format='json', **self.headers)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
