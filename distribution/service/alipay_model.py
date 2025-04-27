import os.path
import time
import traceback
import uuid

import yaml
from alipay import AliPay

from ip_distribution.settings import CONFIG_PATH, BASE_DIR
from ip_distribution.utils.constants_util import WalletOrderStatus
from ip_distribution.utils.exception_util import BusinessException, DataNotExistsException
from ip_distribution.utils.log_util import get_logger
from distribution.models import WalletOrder, User

logger = get_logger("alipay")

with open(CONFIG_PATH, "r") as f:
    application_config = yaml.safe_load(f)
    alipay_config = application_config.get("alipay")

key_path = os.path.join(BASE_DIR, "lib")
app_private_key = open(os.path.join(key_path, "alipay_app_private_key.txt")).read()
public_key = open(os.path.join(key_path, "alipay_public_key.txt")).read()

alipay = AliPay(
    appid=alipay_config.get("app_id"),
    app_notify_url=alipay_config.get("notify_url"),
    app_private_key_string=app_private_key,
    alipay_public_key_string=public_key,
    sign_type=alipay_config.get("sign_type"),
    debug=True,
    verbose=False,
)


class AlipayModel(object):

    def alipay(self, out_trade_no, total_amount, subject):
        """
        创建支付交易，返回alipay的url
        :param out_trade_no: 订单号，保证唯一性
        :param total_amount: 总金额
        :param subject: 当用户被重定向到支付宝页面进行支付时，subject会显示在支付宝的支付确认页面上，让用户知道他们正在为哪个商品或服务付款。
        :return: alipay的url
        """
        logger.info("创建支付宝交易 out_trade_no:{}, total_amount:{}, subject:{}".format(
            out_trade_no, total_amount, subject))
        try:
            order_string = alipay.api_alipay_trade_page_pay(
                out_trade_no=out_trade_no,
                total_amount=total_amount,
                subject=subject,
            )
            logger.info("订单号创建alipay交易成功：{}".format(order_string))
            url = "https://openapi-sandbox.dl.alipaydev.com/gateway.do" + "?" + order_string
            return url
        except Exception as e:
            logger.error("创建支付宝交易失败：{}".format(traceback.format_exc()))
            raise BusinessException("创建支付宝交易失败")

    def async_notify(self, trade_status, out_trade_no, received_amount,
                     trade_no, seller_id, buyer_id):
        """
        处理异步通知
        :param trade_status: 交易状态
        :param out_trade_no: 订单号
        :param received_amount: 收到金额
        :param trade_no: 支付宝交易号
        :return:
        """
        order_status = WalletOrderStatus.PAY_FAILED.value
        if trade_status == "TRADE_SUCCESS":
            logger.info("支付成功，订单号:{}, 支付宝交易号:{}, 收到金额:{}".format(
                out_trade_no, received_amount, trade_no))
            order_status = WalletOrderStatus.PAID.value
        else:
            logger.error("支付失败，状态：{}".format(trade_status))

        # 更新订单信息
        wallet_order = WalletOrder.objects.filter(order_uuid=out_trade_no)
        if not wallet_order.exists():
            raise DataNotExistsException("订单{}不存在".format(out_trade_no))
        wallet_order = wallet_order.first()
        wallet_order.status = order_status
        wallet_order.received_time = int(time.time())
        wallet_order.seller_id = seller_id
        wallet_order.buyer_id = buyer_id
        wallet_order.save()
        logger.info("订单{}状态已更新为：{}".format(out_trade_no, order_status))

        # 新增个人余额
        user_id = wallet_order.user_id
        user = User.objects.get(id=user_id)
        user.balance += float(received_amount)
        user.save()
        logger.info("用户{}余额已更新为：{}".format(user_id, user.balance))


if __name__ == '__main__':
    alipay_model = AlipayModel()
    res = alipay_model.alipay(str(uuid.uuid4()), 100, "测试商品")
    print(res)
