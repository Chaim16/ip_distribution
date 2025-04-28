import json

from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action

from distribution.service.router_model import RouterPortModel
from ip_distribution.utils.log_util import get_logger
from ip_distribution.utils.response import setResult
from ip_distribution.utils.validate import TransCoding

logger = get_logger("router")


class RouterPortViewSet(viewsets.ViewSet):

    @action(methods=['POST'], detail=False)
    @swagger_auto_schema(
        operation_description="新增端口",
        tags=['路由器管理']
    )
    def add(self, request):
        params = json.loads(request.body)
        router_id = params.get("router_id")
        start_addr = params.get("start_addr")
        end_addr = params.get("end_addr")
        mask = params.get("mask", "255.255.255.0")
        gateway = params.get("gateway")
        dns = params.get("dns")
        username = request.user.username
        router_port_model = RouterPortModel()
        router_port_model.add(router_id, start_addr, end_addr, mask, gateway, dns, username)
        return setResult()

    @action(methods=['GET'], detail=False)
    @swagger_auto_schema(
        operation_description="端口详情",
        tags=["路由器管理"],
    )
    def router_port_detail(self, request):
        user = request.user
        if not user.is_authenticated:
            return setResult({}, "用户未登录", 1)
        params = TransCoding().transcoding_dict(dict(request.GET.items()))
        router_port_id = params.get("id")
        router_port_model = RouterPortModel()
        data = router_port_model.detail(router_port_id)
        return setResult(data)

    @action(methods=['POST'], detail=False)
    @swagger_auto_schema(
        operation_description="编辑路由器端口信息",
        tags=['路由器管理']
    )
    def modify(self, request):
        user = request.user
        if not user.is_authenticated:
            return setResult({}, "用户未登录", 1)
        params = json.loads(request.body)
        router_port_id = params.get("id")
        router_id = params.get("router_id")
        start_addr = params.get("start_addr")
        end_addr = params.get("end_addr")
        mask = params.get("mask", "255.255.255.0")
        gateway = params.get("gateway")
        dns = params.get("dns")
        router_port_model = RouterPortModel()
        router_port_model.modity(router_port_id, router_id, start_addr, end_addr, mask, gateway, dns)
        return setResult()

    @action(methods=['GET'], detail=False)
    @swagger_auto_schema(
        operation_description="路由器端口列表",
        tags=['路由器管理']
    )
    def router_port_list(self, request):
        user = request.user
        if not user.is_authenticated:
            return setResult({}, "用户未登录", 1)

        params = TransCoding().transcoding_dict(dict(request.GET.items()))
        page = int(params.get('page', 1))
        size = int(params.get('size', 10))
        router_id_list = params.get('router_id_list', [])
        router_port_model = RouterPortModel()
        data = router_port_model.router_port_list(router_id_list, page, size)
        return setResult(data)

    @action(methods=['POST'], detail=False)
    @swagger_auto_schema(
        operation_description="删除路由器端口",
        tags=['路由器管理']
    )
    def del_router_port(self, request):
        user = request.user
        if not user.is_authenticated:
            return setResult({}, "用户未登录", 1)

        params = json.loads(request.body)
        router_id = params.get("id")
        router_port_model = RouterPortModel()
        router_port_model.del_router_port(router_id)
        return setResult()

