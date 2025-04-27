import os
import random
import time
import uuid

from django.core.files.base import ContentFile
from django.core.paginator import Paginator
from django.forms import model_to_dict

from ip_distribution.utils.constants_util import OrderStatus, Role
from ip_distribution.utils.exception_util import BusinessException
from ip_distribution.utils.log_util import get_logger
from ip_distribution import settings
from distribution.models import User, Draft, Order
from distribution.service.draft_model import DraftModel
from distribution.service.user_model import UserModel

logger = get_logger("ip_distribution")


class OrderModel(object):

    def create_order(self, username, draft_id):
        user = User.objects.get(username=username)
        user_id = user.id

        draft = Draft.objects.get(id=draft_id)
        order_uuid = str(uuid.uuid4())
        params = {
            "user_id": user_id,
            "order_uuid": order_uuid,
            "amount": draft.price,
            "status": OrderStatus.PENDING.value,
            "draft_id": draft_id,
            "create_time": int(time.time()),
            "is_cancel": 0,
        }
        order = Order.objects.create(**params)
        return {"id": order.id}

    def order_list(self, username, page, size, **kwargs):
        user = User.objects.get(username=username)
        role = user.role
        user_id = user.id

        order_list = Order.objects.filter().order_by("-id")
        if kwargs.get("status"):
            order_list = order_list.filter(status=kwargs.get("status"))
        if kwargs.get("draft_id"):
            order_list = order_list.filter(draft_id=kwargs.get("draft_id"))
        if role != Role.ADMINISTRATOR.value:
            order_list = order_list.filter(user_id=user_id)
        count = order_list.count()
        paginator = Paginator(order_list, size)
        order_list = paginator.get_page(page)

        # 获取用户信息
        res = UserModel().user_list(1, 9999)
        user_list = res.get("list", [])
        user_map = {}
        for user in user_list:
            user_map[str(user.get("id"))] = user.get("username")

        # 获取画稿信息
        res = DraftModel().draft_list(1, 9999)
        draft_list = res.get("list", [])
        draft_map = {}
        for draft in draft_list:
            draft_map[str(draft.get("id"))] = draft

        data_list = []
        for item in order_list:
            info = model_to_dict(item)

            draft_id = info.get("draft_id")
            draft_info = draft_map.get(str(draft_id))
            info["draft_title"] = draft_info.get("title")

            info["buyer"] = user_map.get(str(info.get("user_id")))
            info["designer"] = user_map.get(str(draft_info.get("designer_id")))
            data_list.append(info)
        return {"count": count, "list": data_list}

    def pay(self, order_id):
        order = Order.objects.get(id=order_id)
        # 查询画稿详情
        draft_id = order.draft_id
        draft = Draft.objects.get(id=draft_id)

        # 查询买方详情
        user_id = order.user_id
        user = User.objects.get(id=user_id)
        # 如果买方的余额小于画稿的价格，则交易失败
        if user.balance < draft.price:
            raise BusinessException("余额不足")

        user.balance -= draft.price
        user.save()

        # 查询设计师详情，并将amount的金额转入设计师的余额中
        designer_id = draft.designer_id
        designer = User.objects.get(id=designer_id)
        designer.balance += draft.price
        designer.save()

        # 修改订单状态为“已支付”
        order.status = OrderStatus.PAID.value
        order.save()

    def return_order(self, order_id):
        order = Order.objects.get(id=order_id)
        # 查询画稿详情
        draft_id = order.draft_id
        draft = Draft.objects.get(id=draft_id)

        # 查询设计师详情
        designer_id = draft.designer_id
        designer = User.objects.get(id=designer_id)
        # 如果设计师的余额小于画稿的价格，则退回失败
        if designer.balance < draft.price:
            raise BusinessException("余额不足")

        designer.balance -= draft.price
        designer.save()

        # 查询买方详情，，并将amount的金额买方的余额中
        user_id = order.user_id
        user = User.objects.get(id=user_id)

        user.balance += draft.price
        user.save()

        # 修改订单状态为“待支付”
        order.status = OrderStatus.PENDING.value
        order.save()

    def del_order(self, username, order_id):
        order = Order.objects.get(id=order_id)
        user = User.objects.get(username=username)
        user_id = user.id
        if order.user_id != user_id:
            raise BusinessException("无权限删除该订单")
        order.delete()

