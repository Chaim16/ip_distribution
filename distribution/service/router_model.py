import time
import traceback
import uuid

from django.core.paginator import Paginator
from django.forms import model_to_dict

from distribution.models import User, Router
from ip_distribution.utils.constants_util import Role
from ip_distribution.utils.exception_util import BusinessException
from ip_distribution.utils.log_util import get_logger

logger = get_logger("user")


class RouterModel(object):

    def add(self, name, model, location, port_num, username):
        # 判断路由器名称是否存在
        if Router.objects.filter(name=name).exists():
            raise BusinessException("路由器名称{}已存在".format(name))

        add_params = {
            "name": name,
            "model": model,
            "location": location,
            "port_num": port_num,
            "create_time": int(time.time()),
            "create_user": username,
        }
        logger.info("注册用户信息：{}".format(add_params))
        Router.objects.create(**add_params)
        logger.info("注册用户成功：{}".format(username))

    def detail(self, router_id):
        router = Router.objects.get(id=router_id)
        user_dict = {
            "id": router.id,
            "name": router.name,
            "model": router.model,
            "location": router.location,
            "port_num": router.port_num,
            "create_time": router.create_time,
            "create_user": router.create_user,
        }
        return user_dict

    def modify(self, router_id, name, model, location, port_num):

        modify_params = {}
        if name:
            modify_params["name"] = name
        if model:
            modify_params["model"] = model
        if location:
            modify_params["location"] = location
        if port_num:
            modify_params["port_num"] = port_num
        logger.info("修改路由器信息：{}".format(modify_params))
        Router.objects.filter(id=router_id).update(**modify_params)

    def router_list(self, page, size,**kwargs):
        router_list = Router.objects.all().order_by("-id")
        if kwargs.get("name"):
            router_list = router_list.filter(name__icontains=kwargs.get("name"))
        if kwargs.get("model"):
            router_list = router_list.filter(model__icontains=kwargs.get("model"))
        if kwargs.get("location"):
            router_list = router_list.filter(location__icontains=kwargs.get("location"))
        if kwargs.get("port_num"):
            router_list = router_list.filter(port_num=kwargs.get("port_num"))

        count = router_list.count()
        paginator = Paginator(router_list, size)
        router_list = paginator.get_page(page)
        data_list = []
        for item in router_list:
            data_list.append({
                "id": item.id,
                "name": item.name,
                "model": item.model,
                "location": item.location,
                "port_num": item.port_num,
                "create_time": item.create_time,
            })
        return {"count": count, "list": data_list}

    def del_router(self, router_id):
        router = Router.objects.get(id=router_id)
        router.delete()
        logger.info("已删除路由器：{}".format(router))


