import json

from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action

from distribution.service.switch_model import SwitchModel
from ip_distribution.utils.log_util import get_logger
from ip_distribution.utils.response import setResult
from ip_distribution.utils.validate import TransCoding

logger = get_logger("switch")


class SwitchViewSet(viewsets.ViewSet):

    @action(methods=['POST'], detail=False)
    @swagger_auto_schema(
        operation_description="新增",
        tags=['交换机管理']
    )
    def add(self, request):
        params = json.loads(request.body)
        name = params.get("name")
        model = params.get("model")
        location = params.get("location")
        router_id = params.get("router_id")
        router_port_id = params.get("router_port_id")
        department_id = params.get("department_id")
        port_num = params.get("port_num")
        username = request.user.username
        switch_model = SwitchModel()
        switch_model.add(name, model, location, router_id, router_port_id, department_id, port_num, username)
        return setResult()

    @action(methods=['GET'], detail=False)
    @swagger_auto_schema(
        operation_description="交换机详情",
        tags=["交换机管理"],
    )
    def switch_detail(self, request):
        user = request.user
        if not user.is_authenticated:
            return setResult({}, "用户未登录", 1)
        params = TransCoding().transcoding_dict(dict(request.GET.items()))
        switch_id = params.get("id")
        switch_model = SwitchModel()
        data = switch_model.detail(switch_id)
        return setResult(data)

    @action(methods=['POST'], detail=False)
    @swagger_auto_schema(
        operation_description="编辑交换机信息",
        tags=['交换机管理']
    )
    def modify(self, request):
        user = request.user
        if not user.is_authenticated:
            return setResult({}, "用户未登录", 1)
        params = json.loads(request.body)
        switch_id = params.get("id")
        name = params.get("name")
        model = params.get("model")
        location = params.get("location")
        router_id = params.get("router_id")
        router_port_id = params.get("router_port_id")
        department_id = params.get("department_id")
        port_num = params.get("port_num")
        switch_model = SwitchModel()
        switch_model.modify(switch_id, name, model, location, router_id,
                            router_port_id, department_id, port_num)
        return setResult()

    @action(methods=['GET'], detail=False)
    @swagger_auto_schema(
        operation_description="交换机列表",
        tags=['交换机管理']
    )
    def switch_list(self, request):
        user = request.user
        if not user.is_authenticated:
            return setResult({}, "用户未登录", 1)

        params = TransCoding().transcoding_dict(dict(request.GET.items()))
        page = int(params.get('page', 1))
        size = int(params.get('size', 10))
        switch_model = SwitchModel()
        data = switch_model.switch_list(page, size)
        return setResult(data)

    @action(methods=['POST'], detail=False)
    @swagger_auto_schema(
        operation_description="删除路由器端口",
        tags=['交换机管理']
    )
    def del_switch(self, request):
        user = request.user
        if not user.is_authenticated:
            return setResult({}, "用户未登录", 1)

        params = json.loads(request.body)
        switch_id = params.get("id")
        switch_model = SwitchModel()
        switch_model.del_switch(switch_id)
        return setResult()

