import json

from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action

from distribution.service.workstation_model import WorkstationModel
from ip_distribution.utils.log_util import get_logger
from ip_distribution.utils.response import setResult
from ip_distribution.utils.validate import TransCoding

logger = get_logger("workstation")


class WorkstationViewSet(viewsets.ViewSet):

    @action(methods=['POST'], detail=False)
    @swagger_auto_schema(
        operation_description="新增",
        tags=['工位管理']
    )
    def add(self, request):
        params = json.loads(request.body)
        code = params.get("code")
        switch_id = params.get("switch_id")
        location = params.get("location")
        distributed_ip_addr = params.get("distributed_ip_addr")
        user_id = params.get("user_id")
        workstation_model = WorkstationModel()
        workstation_model.add(code, location, switch_id, distributed_ip_addr, user_id)
        return setResult()

    @action(methods=['GET'], detail=False)
    @swagger_auto_schema(
        operation_description="详情",
        tags=["工位管理"],
    )
    def workstation_detail(self, request):
        user = request.user
        if not user.is_authenticated:
            return setResult({}, "用户未登录", 1)
        params = TransCoding().transcoding_dict(dict(request.GET.items()))
        switch_id = params.get("id")
        workstation_model = WorkstationModel()
        data = workstation_model.detail(switch_id)
        return setResult(data)

    @action(methods=['POST'], detail=False)
    @swagger_auto_schema(
        operation_description="编辑",
        tags=['工位管理']
    )
    def modify(self, request):
        user = request.user
        if not user.is_authenticated:
            return setResult({}, "用户未登录", 1)
        params = json.loads(request.body)
        workstation_id = params.get("id")
        code = params.get("code")
        switch_id = params.get("switch_id")
        location = params.get("location")
        distributed_ip_addr = params.get("distributed_ip_addr")
        user_id = params.get("user_id")
        workstation_model = WorkstationModel()
        workstation_model.modify(workstation_id, code, location, switch_id, distributed_ip_addr, user_id)
        return setResult()

    @action(methods=['GET'], detail=False)
    @swagger_auto_schema(
        operation_description="列表",
        tags=['工位管理']
    )
    def workstation_list(self, request):
        user = request.user
        if not user.is_authenticated:
            return setResult({}, "用户未登录", 1)

        params = TransCoding().transcoding_dict(dict(request.GET.items()))
        page = int(params.get('page', 1))
        size = int(params.get('size', 10))
        workstation_model = WorkstationModel()
        data = workstation_model.workstation_list(page, size)
        return setResult(data)

    @action(methods=['POST'], detail=False)
    @swagger_auto_schema(
        operation_description="删除",
        tags=['工位管理']
    )
    def del_workstation(self, request):
        user = request.user
        if not user.is_authenticated:
            return setResult({}, "用户未登录", 1)

        params = json.loads(request.body)
        workstation_id = params.get("id")
        workstation_model = WorkstationModel()
        workstation_model.del_workstation(workstation_id)
        return setResult()

    @action(methods=['POST'], detail=False)
    @swagger_auto_schema(
        operation_description="分配地址",
        tags=['工位管理']
    )
    def distribute(self, request):
        user = request.user
        if not user.is_authenticated:
            return setResult({}, "用户未登录", 1)

        params = json.loads(request.body)
        switch_id = params.get("switch_id")
        workstation_model = WorkstationModel()
        data = workstation_model.distribute(switch_id)
        return setResult(data)
