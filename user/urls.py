from rest_framework.routers import DefaultRouter
from . import views

app_name = 'user'

router = DefaultRouter(trailing_slash=False)
router.register(r'groups', views.GroupView)
router.register(r'users', views.UserView)

urlpatterns = router.urls
