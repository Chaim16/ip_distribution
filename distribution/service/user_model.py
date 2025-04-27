import time
import traceback
import uuid

from django.core.paginator import Paginator
from django.forms import model_to_dict

from ip_distribution.utils.constants_util import Role, DesignerApplicationStatus, WalletOrderStatus
from ip_distribution.utils.exception_util import BusinessException
from ip_distribution.utils.log_util import get_logger
from distribution.models import User, DesignerApplicationRecord, WalletOrder, Order
from distribution.service.alipay_model import AlipayModel

logger = get_logger("user")


class UserModel(object):

    def register(self, username, password, nickname, gender, phone):
        # 判断用户是否存在
        if User.objects.filter(username=username).exists():
            raise BusinessException("用户名{}已存在".format(username))

        # 保存用户信息
        add_params = {
            "username": username,
            "password": password,
            "nickname": nickname,
            "gender": gender,
            "phone": phone,
            "role": Role.GENERAL.value,
        }
        logger.info("注册用户信息：{}".format(add_params))
        User.objects.create_user(**add_params)
        logger.info("注册用户成功：{}".format(username))

    def whoami(self, username):
        user = User.objects.get(username=username)
        return {
            "username": user.username,
            "role": user.role,
        }

    def detail(self, username):
        user = User.objects.get(username=username)
        user_dict = {
            "username": user.username,
            "nickname": user.nickname,
            "gender": user.gender,
            "phone": user.phone,
            "role": user.role,
            "balance": user.balance,
        }
        return user_dict

    def modify(self, username, nickname, gender, phone, role):

        modify_params = {}
        if nickname:
            modify_params["nickname"] = nickname
        if gender is not None:
            modify_params["gender"] = gender
        if phone:
            modify_params["phone"] = phone
        if role:
            modify_params["role"] = role
        logger.info("修改用户信息：{}".format(modify_params))
        User.objects.filter(username=username).update(**modify_params)

    def id_by_username(self, username):
        user = User.objects.get(username=username)
        return user.id

    def designer_application_record(self, username):
        user_id = self.id_by_username(username)
        record = DesignerApplicationRecord.objects.filter(user_id=user_id)
        if not record.exists():
            return {}
        record = record.first()
        record_dict = model_to_dict(record)
        return record_dict

    def apply_as_designer(self, username, reason):
        user_id = self.id_by_username(username)
        params = {
            "user_id": user_id,
            "reason": reason,
            "status": DesignerApplicationStatus.WAIT_APPROVAL.value,
            "create_time": int(time.time()),
        }
        record = DesignerApplicationRecord.objects.create(**params)
        return {"id": record.id}

    def recharge(self, username, amount):
        user_id = self.id_by_username(username)
        order_uuid = str(uuid.uuid4())
        params = {
            "order_uuid": order_uuid,
            "status": WalletOrderStatus.PENDING.value,
            "user_id": user_id,
            "amount": amount,
            "create_time": int(time.time()),
        }
        try:
            logger.info("创建充值订单：{}".format(params))
            WalletOrder.objects.create(**params)
            logger.info("充值订单创建成功")

            alipay_model = AlipayModel()
            url = alipay_model.alipay(order_uuid, amount, "余额充值")
            return {"url": url}
        except Exception as e:
            logger.error("创建充值订单失败：{}".format(traceback.format_exc()))
            raise BusinessException("创建充值订单失败")

    def apply_designer_list(self, page, size, **kwargs):
        record_list = DesignerApplicationRecord.objects.filter().order_by("-id")
        if kwargs.get("status"):
            record_list = record_list.filter(status=kwargs.get("status"))
        if kwargs.get("user_id"):
            record_list = record_list.filter(user_id=kwargs.get("user_id"))
        count = record_list.count()
        paginator = Paginator(record_list, size)
        record_list = paginator.get_page(page)

        # 获取用户列表
        res = self.user_list(1, 9999)
        user_list = res.get("list", [])
        user_map = {}
        for user in user_list:
            user_map[str(user.get("id"))] = user.get("username")

        data_list = []
        for item in record_list:
            info = model_to_dict(item)
            username = user_map.get(str(info.get("user_id")))
            info["username"] = username
            data_list.append(info)
        return {"count": count, "list": data_list}

    def approve_designer_application(self, record_id, status, approval_opinions):
        record = DesignerApplicationRecord.objects.get(id=record_id)
        record.status = status
        record.approval_opinions = approval_opinions
        record.approval_time = int(time.time())
        record.save()
        logger.info("更新设计师申请记录, record_id: {}, status: {}, approval_opinions: {}".format(
            record_id, status, approval_opinions
        ))
        User.objects.filter(id=record.user_id).update(role=Role.DESIGNER.value)

    def user_list(self, page, size,**kwargs):
        user_list = User.objects.all().order_by("-id")
        if kwargs.get("username"):
            user_list = user_list.filter(username=kwargs.get("username"))
        if kwargs.get("gender") is not None:
            user_list = user_list.filter(gender=kwargs.get("gender"))
        if kwargs.get("phone"):
            user_list = user_list.filter(phone=kwargs.get("phone"))
        if kwargs.get("role"):
            user_list = user_list.filter(role=kwargs.get("role"))
        count = user_list.count()
        paginator = Paginator(user_list, size)
        user_list = paginator.get_page(page)
        data_list = []
        for item in user_list:
            data_list.append({
                "id": item.id,
                "username": item.username,
                "nickname": item.nickname,
                "gender": item.gender,
                "phone": item.phone,
                "role": item.role,
                "balance": item.balance,
            })
        return {"count": count, "list": data_list}

    def del_user(self, username):
        user = User.objects.get(username=username)
        user_id = user.id
        # 删除关联的设计师申请
        DesignerApplicationRecord.objects.filter(user_id=user_id).delete()
        # 删除关联的订单
        Order.objects.filter(user_id=user_id).delete()
        user.delete()
        logger.info("已删除用户：{}".format(username))


