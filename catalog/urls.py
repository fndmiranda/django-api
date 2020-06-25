from django.urls import path
from .views import ProductViewSet, CategoryViewSet

app_name = 'catalog'

category_list = CategoryViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

category_detail = CategoryViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

product_list = ProductViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

product_detail = ProductViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('categories', category_list, name='category-list'),
    path('categories/<int:pk>', category_detail, name='category-detail'),
    path('products', product_list, name='product-list'),
    path('products/<int:pk>', product_detail, name='product-detail'),
]
