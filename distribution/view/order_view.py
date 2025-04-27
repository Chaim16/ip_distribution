import json
import traceback

from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action

from ip_distribution.utils.exception_util import BusinessException
from ip_distribution.utils.log_util import get_logger
from ip_distribution.utils.response import setResult
from ip_distribution.utils.validate import TransCoding
from distribution.service.order_model import OrderModel
from distribution.view.serilazer import CreateOrderSerializer, OrderDeleteSerializer

logger = get_logger("home")


class OrderViewSet(viewsets.ViewSet):

    @action(methods=['POST'], detail=False)
    @swagger_auto_schema(
        operation_description="创建订单",
        request_body=CreateOrderSerializer,
        tags=["订单管理"],
    )
    def create_order(self, request):
        user = request.user
        if not user.is_authenticated:
            return setResult({}, "用户未登录", 1)

        params = json.loads(request.body)
        draft_id = params.get("draft_id", "")
        username = user.username

        order_model = OrderModel()
        try:
            data = order_model.create_order(username, draft_id)
            return setResult(data)
        except Exception as e:
            logger.error("创建订单失败：{}".format(traceback.format_exc()))
            raise BusinessException("创建订单失败")

    @action(methods=['GET'], detail=False)
    @swagger_auto_schema(
        operation_description="订单列表",
        tags=['订单管理']
    )
    def order_list(self, request):
        user = request.user
        if not user.is_authenticated:
            return setResult({}, "用户未登录", 1)

        params = TransCoding().transcoding_dict(dict(request.GET.items()))
        page = int(params.get('page', 1))
        size = int(params.get('size', 10))
        username = user.username
        order_model = OrderModel()
        try:
            data = order_model.order_list(username, page, size)
            return setResult(data)
        except Exception as e:
            logger.error("获取订单列表失败：{}".format(traceback.format_exc()))
            raise BusinessException("获取订单列表失败")

    @action(methods=['POST'], detail=False)
    @swagger_auto_schema(
        operation_description="支付",
        request_body=CreateOrderSerializer,
        tags=["订单管理"],
    )
    def pay(self, request):
        user = request.user
        if not user.is_authenticated:
            return setResult({}, "用户未登录", 1)

        params = json.loads(request.body)
        order_id = params.get("order_id", "")
        order_model = OrderModel()
        try:
            order_model.pay(order_id)
            return setResult()
        except Exception as e:
            logger.error("支付失败：{}".format(traceback.format_exc()))
            raise BusinessException("支付失败")

    @action(methods=['POST'], detail=False)
    @swagger_auto_schema(
        operation_description="退回",
        request_body=CreateOrderSerializer,
        tags=["订单管理"],
    )
    def return_order(self, request):
        user = request.user
        if not user.is_authenticated:
            return setResult({}, "用户未登录", 1)

        params = json.loads(request.body)
        order_id = params.get("order_id", "")
        order_model = OrderModel()
        try:
            order_model.return_order(order_id)
            return setResult()
        except Exception as e:
            logger.error("退回失败：{}".format(traceback.format_exc()))
            raise BusinessException("退回失败")

    @action(methods=['POST'], detail=False)
    @swagger_auto_schema(
        operation_description="删除订单",
        request_body=OrderDeleteSerializer,
        tags=["订单管理"],
    )
    def del_order(self, request):
        user = request.user
        if not user.is_authenticated:
            return setResult({}, "用户未登录", 1)

        params = json.loads(request.body)
        order_id = params.get("order_id", "")
        username = user.username
        order_model = OrderModel()
        try:
            order_model.del_order(username, order_id)
            return setResult()
        except Exception as e:
            logger.error("删除订单失败：{}".format(traceback.format_exc()))
            raise BusinessException("删除订单失败")

