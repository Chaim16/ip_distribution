import time

from django.core.paginator import Paginator
from django.forms import model_to_dict

from distribution.models import Router, RouterPort
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
        logger.info("添加路由器信息：{}".format(add_params))
        router = Router.objects.create(**add_params)
        # 保存端口
        ports = []
        for item in range(port_num):
            port = RouterPort()
            port.code = "G/{}".format(item)
            port.router_id = router.id
            port.create_time = int(time.time())
            port.create_user = username
            ports.append(port)
        RouterPort.objects.bulk_create(ports)
        logger.info("添加路由器成功：{}, port_list:{}".format(add_params, ports))

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

    def router_list(self, page, size, **kwargs):
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


class RouterPortModel(object):

    def add(self, router_id, start_addr, end_addr, mask, gateway, dns, username):
        add_params = {
            "router_id": router_id,
            "start_addr": start_addr,
            "end_addr": end_addr,
            "mask": mask,
            "gateway": gateway,
            "dns": dns,
            "create_time": int(time.time()),
            "create_user": username,
        }
        logger.info("添加端口信息：{}".format(add_params))
        RouterPort.objects.create(**add_params)
        logger.info("添加端口信息：{}".format(username))

    def modity(self, router_port_id, router_id, start_addr, end_addr, mask, gateway, dns):
        modify_params = {}
        if router_id:
            modify_params["router_id"] = router_id
        if start_addr:
            modify_params["start_addr"] = start_addr
        if end_addr:
            modify_params["end_addr"] = end_addr
        if mask:
            modify_params["mask"] = mask
        if gateway:
            modify_params["gateway"] = gateway
        if dns:
            modify_params["dns"] = dns
        logger.info("修改路由器端口信息：{}".format(modify_params))
        RouterPort.objects.filter(id=router_port_id).update(**modify_params)

    def detail(self, port_id):
        router_port = RouterPort.objects.get(id=port_id)
        logger.info("获取路由器端口信息：{}".format(router_port))
        router = Router.objects.get(id=router_port.router_id)
        router_port_info = model_to_dict(router_port)
        router_port_info["router_name"] = router.name
        return router_port_info

    def router_port_list(self, router_id, page, size, **kwargs):
        router_port_list = RouterPort.objects.all().order_by("-id")
        if router_id:
            router_port_list = router_port_list.filter(router_id=router_id)

        router_map = {}
        router_all = Router.objects.all()
        for item in router_all:
            router_map[item.id] = item.name

        count = router_port_list.count()
        paginator = Paginator(router_port_list, size)
        router_port_list = paginator.get_page(page)
        data_list = []
        for item in router_port_list:
            data_list.append({
                "id": item.id,
                "code": item.code,
                "router_name": router_map.get(item.router_id),
                "router_id": item.router_id,
                "start_addr": item.start_addr,
                "end_addr": item.end_addr,
                "mask": item.mask,
                "gateway": item.gateway,
                "dns": item.dns,
                "create_time": item.create_time,
                "create_user": item.create_user,
            })
        return {"count": count, "list": data_list}

    def del_router_port(self, port_id):
        port = RouterPort.objects.get(id=port_id)
        port.delete()
        logger.info("已删除路由器端口：{}".format(port))

