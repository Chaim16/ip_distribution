from rest_framework.routers import DefaultRouter

from distribution.view.router_port_view import RouterPortViewSet
from distribution.view.router_view import RouterViewSet
from distribution.view.switch_view import SwitchViewSet
from distribution.view.user_view import UserViewSet
from distribution.view.workstation_view import WorkstationViewSet

router = DefaultRouter()

urlpatterns = []
router.register(r'api/v1/user', UserViewSet, basename="user")
router.register(r'api/v1/router', RouterViewSet, basename="router")
router.register(r'api/v1/router_port', RouterPortViewSet, basename="router")
router.register(r'api/v1/switch', SwitchViewSet, basename="router")
router.register(r'api/v1/workstation', WorkstationViewSet, basename="router")

urlpatterns += router.urls
