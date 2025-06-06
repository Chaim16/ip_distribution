import time

from django.core.paginator import Paginator
from django.forms import model_to_dict

from distribution.models import Router, RouterPort, Switch, Workstation
from ip_distribution.utils.exception_util import BusinessException
from ip_distribution.utils.log_util import get_logger

logger = get_logger("user")


class SwitchModel(object):

    def add(self, name, code, model, location, router_id, router_port_id, port_num, username):
        # 判断交换机名称是否存在
        if Switch.objects.filter(name=name).exists():
            raise BusinessException("路由器名称{}已存在".format(name))

        add_params = {
            "name": name,
            "code": code,
            "model": model,
            "location": location,
            "router_id": router_id,
            "router_port_id": router_port_id,
            "port_num": port_num,
            "create_time": int(time.time()),
            "create_user": username,
        }
        logger.info("添加交换机信息：{}".format(add_params))
        Switch.objects.create(**add_params)
        logger.info("添加交换机成功：{}".format(username))

    def detail(self, switch_id):
        switch = Switch.objects.get(id=switch_id)
        switch_info = model_to_dict(switch)
        logger.info("获取交换机信息：{}".format(switch_info))

        router = Router.objects.get(id=switch.router_id)
        router_port = RouterPort.objects.get(id=switch.router_port_id)

        switch_info["router_name"] = router.name
        switch_info["router_port_code"] = router_port.code
        switch_info["start_addr"] = router_port.start_addr
        switch_info["end_addr"] = router_port.end_addr
        switch_info["dns"] = router_port.dns
        switch_info["gateway"] = router_port.gateway
        switch_info["mask"] = router_port.mask
        return switch_info

    def modify(self, switch_id, name, code, model, location, router_id, router_port_id, port_num):
        modify_params = {}
        if name:
            modify_params["name"] = name
        if code:
            modify_params["code"] = code
        if model:
            modify_params["model"] = model
        if location:
            modify_params["location"] = location
        if router_id:
            modify_params["router_id"] = router_id
        if router_port_id:
            modify_params["router_port_id"] = router_port_id
        if port_num:
            modify_params["port_num"] = port_num
        logger.info("修改交换机信息：{}".format(modify_params))
        Switch.objects.filter(id=switch_id).update(**modify_params)

    def switch_list(self, page, size, **kwargs):
        switch_list = Switch.objects.all().order_by("-id")
        if kwargs.get("name"):
            switch_list = switch_list.filter(name__icontains=kwargs.get("name"))
        if kwargs.get("model"):
            switch_list = switch_list.filter(model__icontains=kwargs.get("model"))
        if kwargs.get("location"):
            switch_list = switch_list.filter(location__icontains=kwargs.get("location"))
        if kwargs.get("port_num"):
            switch_list = switch_list.filter(port_num=kwargs.get("port_num"))

        router_map = {}
        router_list = Router.objects.all()
        for item in router_list:
            router_map[item.id] = item.name
        router_port_map = {}
        router_port_list = RouterPort.objects.all()
        for item in router_port_list:
            router_port_map[item.id] = model_to_dict(item)

        count = switch_list.count()
        paginator = Paginator(switch_list, size)
        switch_list = paginator.get_page(page)
        data_list = []
        for item in switch_list:
            obj = model_to_dict(item)
            router_port = router_port_map.get(obj.get("router_port_id"))

            obj["router_name"] = router_map.get(obj.get("router_id"))
            obj["router_port_code"] = router_port.get("code")
            obj["start_addr"] = router_port.get("start_addr")
            obj["end_addr"] = router_port.get("end_addr")
            obj["dns"] = router_port.get("dns")
            obj["gateway"] = router_port.get("gateway")
            obj["mask"] = router_port.get("mask")
            data_list.append(obj)

        return {"count": count, "list": data_list}

    def del_switch(self, switch_id):
        if Workstation.objects.filter(switch_id=switch_id).exists():
            raise BusinessException("该交换机已被工位使用，不能删除")
        switch = Switch.objects.get(id=switch_id)
        switch.delete()
        logger.info("已删除交换机：{}".format(switch))

