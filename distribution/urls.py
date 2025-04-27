from rest_framework.routers import DefaultRouter

from distribution.view.alipay_view import AlipayViewSet
from distribution.view.draft_view import DraftViewSet
from distribution.view.home_view import HomeViewSet
from distribution.view.order_view import OrderViewSet
from distribution.view.user_view import UserViewSet

router = DefaultRouter()

urlpatterns = []
router.register(r'api/v1/user', UserViewSet, basename="user")
router.register(r'api/v1/home', HomeViewSet, basename="home")
router.register(r'api/v1/alipay', AlipayViewSet, basename="alipay")
router.register(r'api/v1/ip_distribution', DraftViewSet, basename="ip_distribution")
router.register(r'api/v1/order', OrderViewSet, basename="order")
urlpatterns += router.urls
