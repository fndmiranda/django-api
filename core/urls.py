from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls import url
from django.conf.urls import include
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from accounts import views as accounts
from users import views as users

schema_view = get_schema_view(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer]
)

router = DefaultRouter(trailing_slash=False)
router.register(r'users', users.UserViewSet)
router.register(r'groups', users.GroupViewSet)
router.register(r'accounts', accounts.AccountViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^oauth2/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^', include(router.urls)),
    url(r'^schema/$', schema_view),
    url(r'^docs/', include_docs_urls(title=settings.APP_NAME, description=settings.APP_DESCRIPTION)),
]
