import logging
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer, ProductWriteSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

logger = logging.getLogger('catalog.views')


class CategoryViewSet(ModelViewSet):
    """
    A viewset for viewing and editing catalog category instances.

    list:
    Return the list of category instance.

    read:
    Return the specific category instance.

    create:
    Create a new category instance.

    update:
    Update a category instance.

    partial_update:
    Partial update a category instance.

    delete:
    Delete a category instance.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        logger.info('Starting list {} with params: {}'.format(
            Category._meta.verbose_name_plural.title(), request.query_params.dict())
        )
        response = super().list(request, *args, **kwargs)
        logger.info('Response list {} with status code: {} params: {} response: {}'.format(
            Category._meta.verbose_name_plural.title(), response.status_code, request.query_params.dict(), response.data
        ))
        return response

    def create(self, request, *args, **kwargs):
        logger.info('Starting create a {} with payload: {} user id: {}'.format(
            Category._meta.verbose_name.title(), request.data, request.user.id)
        )
        response = super().create(request, *args, **kwargs)
        logger.info('Response create a {} with status code: {} response: {} user id: {}'.format(
            Category._meta.verbose_name.title(), response.status_code, response.data, request.user.id
        ))
        return response

    def retrieve(self, request, *args, **kwargs):
        logger.info('Starting retrieve a {} with pk: {}'.format(Category._meta.verbose_name.title(), kwargs['pk']))
        response = super().retrieve(request, *args, **kwargs)
        logger.info('Response retrieve a {} with pk: {} status code: {} response: {}'.format(
            Category._meta.verbose_name.title(), kwargs['pk'], response.status_code, response.data
        ))
        return response

    def update(self, request, *args, **kwargs):
        action = 'partial update' if kwargs.get('partial', False) else 'update'
        logger.info('Starting {} a {} with pk: {} payload: {} user id: {}'.format(
            Category._meta.verbose_name.title(), action, kwargs['pk'], request.data, request.user.id
        ))
        response = super().update(request, *args, **kwargs)
        logger.info('Response {} a {} with pk: {} status code: {} response: {} user id: {}'.format(
            Category._meta.verbose_name.title(), action, kwargs['pk'], response.status_code, response.data, request.user.id
        ))
        return response

    def destroy(self, request, *args, **kwargs):
        logger.info('Starting destroy a {} with pk: {} user id'.format(
            Category._meta.verbose_name.title(), kwargs['pk'], request.user.id)
        )
        response = super().destroy(request, *args, **kwargs)
        logger.info('Response destroy a {} with pk: {} status code: {} user id: {}'.format(
            Category._meta.verbose_name.title(), kwargs['pk'], response.status_code, request.user.id
        ))
        return response


class ProductViewSet(ModelViewSet):
    """
    A viewset for viewing and editing catalog product instances.

    list:
    Return the list of product instance.

    read:
    Return the specific product instance.

    create:
    Create a new product instance.

    update:
    Update a product instance.

    partial_update:
    Partial update a product instance.

    delete:
    Delete a product instance.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        return serializer.save()

    def perform_update(self, serializer):
        return serializer.save()

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        logger.info('Starting list {} with params: {}'.format(
            Product._meta.verbose_name_plural.title(), request.query_params.dict())
        )
        response = super().list(request, *args, **kwargs)
        logger.info('Response list {} with status code: {} params: {} response: {}'.format(
            Product._meta.verbose_name_plural.title(), response.status_code, request.query_params.dict(), response.data
        ))
        return response

    @swagger_auto_schema(request_body=ProductWriteSerializer, responses={201: ProductSerializer})
    def create(self, request, *args, **kwargs):
        logger.info('Starting create a {} with payload: {} user id: {}'.format(
            Product._meta.verbose_name.title(), request.data, request.user.id)
        )
        serializer_write = ProductWriteSerializer(data=request.data)
        serializer_write.is_valid(raise_exception=True)
        instance = self.perform_create(serializer_write)
        serializer = ProductSerializer(instance)
        headers = self.get_success_headers(serializer_write.data)

        logger.info('Response create a {} with status code: {} response: {} user id: {}'.format(
            Product._meta.verbose_name.title(), status.HTTP_201_CREATED, serializer.data, request.user.id
        ))
        return Response(data=serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        logger.info('Starting retrieve a {} with pk: {}'.format(Product._meta.verbose_name.title(), kwargs['pk']))
        response = super().retrieve(request, *args, **kwargs)
        logger.info('Response retrieve a {} with pk: {} status code: {} response: {}'.format(
            Product._meta.verbose_name.title(), kwargs['pk'], response.status_code, response.data
        ))
        return response

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        action = 'partial update' if partial else 'update'
        logger.info('Starting {} a {} with pk: {} payload: {} user id: {}'.format(
            Product._meta.verbose_name.title(), action, kwargs['pk'], request.data, request.user.id
        ))
        instance = self.get_object()
        serializer_write = ProductWriteSerializer(instance, data=request.data, partial=partial)
        serializer_write.is_valid(raise_exception=True)
        instance = self.perform_update(serializer_write)
        serializer = ProductSerializer(instance)

        logger.info('Response {} a {} with pk: {} status code: {} response: {} user id: {}'.format(
            Product._meta.verbose_name.title(), action, kwargs['pk'], status.HTTP_200_OK, serializer.data,
            request.user.id
        ))
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        logger.info('Starting destroy a {} with pk: {} user id'.format(
            Product._meta.verbose_name.title(), kwargs['pk'], request.user.id)
        )
        response = super().destroy(request, *args, **kwargs)
        logger.info('Response destroy a {} with pk: {} status code: {} user id: {}'.format(
            Product._meta.verbose_name.title(), kwargs['pk'], response.status_code, request.user.id
        ))
        return response
