from rest_framework.routers import DefaultRouter

from distribution.view.router_view import RouterViewSet
from distribution.view.user_view import UserViewSet


router = DefaultRouter()

urlpatterns = []
router.register(r'api/v1/user', UserViewSet, basename="user")
router.register(r'api/v1/router', RouterViewSet, basename="router")
urlpatterns += router.urls
