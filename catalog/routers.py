from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter(trailing_slash=False)
router.register(r'catalog/products', views.ProductViewSet)
router.register(r'catalog/categories', views.CategoryViewSet)
