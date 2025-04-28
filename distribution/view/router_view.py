import json
import traceback

from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action

from distribution.service.router_model import RouterModel
from ip_distribution.utils.constants_util import Role
from ip_distribution.utils.exception_util import BusinessException, ParamsException
from ip_distribution.utils.log_util import get_logger
from ip_distribution.utils.response import setResult
from ip_distribution.utils.validate import TransCoding
from distribution.service.user_model import UserModel

logger = get_logger("router")


class RouterViewSet(viewsets.ViewSet):

    @action(methods=['POST'], detail=False)
    @swagger_auto_schema(
        operation_description="新增",
        tags=['路由器管理']
    )
    def add(self, request):
        params = json.loads(request.body)
        name = params.get("name")
        model = params.get("model")
        location = params.get("location")
        port_num = params.get("port_num")
        username = request.user.username
        router_model = RouterModel()
        router_model.add(name, model, location, port_num, username)
        return setResult()

    @action(methods=['GET'], detail=False)
    @swagger_auto_schema(
        operation_description="detail",
        tags=["路由器管理"],
    )
    def router_detail(self, request):
        user = request.user
        if not user.is_authenticated:
            return setResult({}, "用户未登录", 1)
        params = TransCoding().transcoding_dict(dict(request.GET.items()))
        router_id = params.get("id")
        router_model = RouterModel()
        data = router_model.detail(router_id)
        return setResult(data)

    @action(methods=['POST'], detail=False)
    @swagger_auto_schema(
        operation_description="编辑路由器信息",
        tags=['路由器管理']
    )
    def modify(self, request):
        user = request.user
        if not user.is_authenticated:
            return setResult({}, "用户未登录", 1)

        params = json.loads(request.body)
        router_id = params.get("id")
        name = params.get("name")
        model = params.get("model")
        location = params.get("location")
        port_num = params.get("port_num")
        router_model = RouterModel()
        router_model.modify(router_id, name, model, location, port_num)
        return setResult()

    @action(methods=['GET'], detail=False)
    @swagger_auto_schema(
        operation_description="路由器列表",
        tags=['路由器管理']
    )
    def router_list(self, request):
        user = request.user
        if not user.is_authenticated:
            return setResult({}, "用户未登录", 1)

        params = TransCoding().transcoding_dict(dict(request.GET.items()))
        page = int(params.get('page', 1))
        size = int(params.get('size', 10))
        router_model = RouterModel()
        data = router_model.router_list(page, size)
        return setResult(data)

    @action(methods=['POST'], detail=False)
    @swagger_auto_schema(
        operation_description="删除用户",
        tags=['用户管理']
    )
    def del_router(self, request):
        user = request.user
        if not user.is_authenticated:
            return setResult({}, "用户未登录", 1)

        params = json.loads(request.body)
        router_id = params.get("id")
        router_model = RouterModel()
        router_model.del_router(router_id)
        return setResult()

