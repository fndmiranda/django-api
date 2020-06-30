from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls import url
from django.conf.urls import include
from rest_framework.decorators import api_view
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.documentation import include_docs_urls

schema_view = get_schema_view(
   openapi.Info(
      title=settings.APP_NAME,
      default_version='v1',
      description=settings.APP_DESCRIPTION,
      terms_of_service='https://www.google.com/policies/terms/',
      contact=openapi.Contact(email='fndmiranda@gmail.com'),
      license=openapi.License(name='BSD License'),
   ),
   public=True,
   permission_classes=(permissions.IsAuthenticated,),
)


@api_view(['GET'])
def index(request):
    return Response({'running'}, status=status.HTTP_200_OK)


urlpatterns = [
    url(r'^$', index),
    path('admin/', admin.site.urls),
    url(r'^catalog/', include('catalog.urls', namespace='catalog')),
    url(r'^account/', include('account.urls', namespace='account')),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^oauth2/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^docs/', include_docs_urls(title=settings.APP_NAME, description=settings.APP_DESCRIPTION), name='docs-ui'),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='swagger-without-ui'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='redoc-ui'),
]
