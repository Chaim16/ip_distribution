import traceback

from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, permissions
from rest_framework.decorators import action

from ip_distribution.utils.exception_util import BusinessException
from ip_distribution.utils.log_util import get_logger
from ip_distribution.utils.response import setResult
from distribution.service.alipay_model import AlipayModel

logger = get_logger("alipay")


class AlipayViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    @action(methods=['POST'], detail=False)
    @swagger_auto_schema(
        operation_description="支付异步回调",
        tags=["支付宝"],
    )
    def notify(self, request):
        # 获取所有参数
        params = request.POST.dict()
        logger.info("收到支付异步回调请求：{}".format(params))

        out_trade_no = params.get("out_trade_no")
        receipt_amount = params.get("receipt_amount")
        trade_no = params.get("trade_no")
        trade_status = params.get("trade_status")
        seller_id = params.get("seller_id")
        buyer_id = params.get("buyer_id")
        try:
            AlipayModel().async_notify(trade_status, out_trade_no, receipt_amount, trade_no, seller_id, buyer_id)
            return setResult()
        except Exception as e:
            logger.error("支付异步回调请求处理失败：{}".format(traceback.format_exc()))
            raise BusinessException("支付异步回调请求处理失败")
