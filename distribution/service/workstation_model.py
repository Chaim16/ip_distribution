import ipaddress
import time

from django.core.paginator import Paginator
from django.forms import model_to_dict

from distribution.models import Router, RouterPort, Switch, Workstation, SwitchPort, User
from ip_distribution.utils.exception_util import BusinessException
from ip_distribution.utils.log_util import get_logger

logger = get_logger("workstation")


class WorkstationModel(object):

    def add(self, code, location, switch_id, distributed_ip_addr, user_id):
        # 创建交换机端口
        add_params = {
            "switch_id": switch_id,
            "ip_addr": distributed_ip_addr,
        }
        switch_port = SwitchPort.objects.create(**add_params)
        logger.info("创建交换机端口成功：{}".format(switch_port))
        add_params = {
            "code": code,
            "switch_id": switch_id,
            "switch_port_id": switch_port.id,
            "location": location,
            "user_id": user_id,
        }
        logger.info("添加工位信息：{}".format(add_params))
        Workstation.objects.create(**add_params)
        logger.info("添加工位成功：{}".format(add_params))

    def detail(self, workstation_id):
        workstation = Workstation.objects.get(id=workstation_id)
        workstation_info = model_to_dict(workstation)

        switch_port = SwitchPort.objects.get(id=workstation.switch_port_id)
        switch = Switch.objects.get(id=switch_port.switch_id)
        router_port = RouterPort.objects.get(id=switch.router_port_id)
        user = User.objects.get(id=workstation.user_id)

        workstation_info["switch_name"] = switch.name
        workstation_info["ip_addr"] = switch_port.ip_addr
        workstation_info["dns"] = router_port.dns
        workstation_info["mask"] = router_port.mask
        workstation_info["gateway"] = router_port.gateway
        workstation_info["user_nickname"] = user.nickname
        workstation_info["user_id"] = user.id
        return workstation_info

    def modify(self, workstation_id, code, location, switch_id, distributed_ip_addr, user_id):
        modify_params = {}
        # 查出并删除之前关联的交换机端口
        workstation = Workstation.objects.get(id=workstation_id)
        switch_port = SwitchPort.objects.get(id=workstation.switch_port_id)
        logger.info("工位{}之前关联的交换机端口：{}".format(workstation.code, switch_port))
        if switch_port.ip_addr != distributed_ip_addr:
            switch_port.delete()
            logger.info("已删除工位关联的交换机端口：{}").format(switch_port)
            # 创建新的交换机端口
            add_params = {
                "switch_id": switch_id,
                "ip_addr": distributed_ip_addr,
            }
            switch_port = SwitchPort.objects.create(**add_params)
            logger.info("创建交换机端口成功：{}".format(switch_port))
            modify_params["switch_port_id"] = switch_port.id
        if code:
            modify_params["code"] = code
        if location:
            modify_params["location"] = location
        if switch_id:
            modify_params["switch_id"] = switch_id
        if user_id:
            modify_params["user_id"] = user_id
        logger.info("修改交换机信息：{}".format(modify_params))
        Workstation.objects.filter(id=workstation_id).update(**modify_params)

    def workstation_list(self, page, size, **kwargs):
        workstation_list = Workstation.objects.all().order_by("-id")
        if kwargs.get("code"):
            workstation_list = workstation_list.filter(code__icontains=kwargs.get("code"))
        if kwargs.get("location"):
            workstation_list = workstation_list.filter(location__icontains=kwargs.get("location"))

        switch_map = {}
        switch_list = Switch.objects.all()
        for item in switch_list:
            switch_map[str(item.id)] = model_to_dict(item)
        switch_port_map = {}
        switch_port_list = SwitchPort.objects.all()
        for item in switch_port_list:
            switch_port_map[str(item.id)] = model_to_dict(item)
        router_port_map = {}
        router_port_list = RouterPort.objects.all()
        for item in router_port_list:
            router_port_map[str(item.id)] = model_to_dict(item)
        user_map = {}
        user_list = User.objects.all()
        for item in user_list:
            user_map[str(item.id)] = model_to_dict(item)

        logger.debug("交换机信息：{}".format(switch_map))
        logger.debug("交换机端口信息：{}".format(switch_port_map))
        logger.debug("路由器端口信息：{}".format(router_port_map))

        count = workstation_list.count()
        paginator = Paginator(workstation_list, size)
        workstation_list = paginator.get_page(page)
        data_list = []
        for item in workstation_list:
            obj = model_to_dict(item)
            switch_info = switch_map.get(str(obj.get("switch_id")))
            switch_port_info = switch_port_map.get(str(obj.get("switch_port_id")))
            router_port_info = router_port_map.get(str(switch_info.get("router_port_id")))
            user_info = user_map.get(str(obj.get("user_id")))

            obj["switch_name"] = switch_map.get("name")
            obj["ip_addr"] = switch_port_info.get("ip_addr")
            obj["dns"] = router_port_info.get("dns")
            obj["gateway"] = router_port_info.get("gateway")
            obj["mask"] = router_port_info.get("mask")
            obj["username"] = user_info.get("username")
            obj["user_id"] = user_info.get("id")
            obj["user_nickname"] = user_info.get("nickname")
            data_list.append(obj)

        return {"count": count, "list": data_list}

    def del_workstation(self, workstation_id):
        workstation = Workstation.objects.get(id=workstation_id)
        # 删除关联的交换机端口
        switch_port = SwitchPort.objects.get(id=workstation.switch_port_id)
        switch_port.delete()
        logger.info("已删除工位关联的交换机端口：{}".format(switch_port))
        workstation.delete()
        logger.info("已删除工位：{}".format(workstation))

    def distribute(self, switch_id):
        switch = Switch.objects.get(id=switch_id)
        logger.info("获取交换机信息：{}".format(switch))

        router_port_id = switch.router_port_id
        router_port = RouterPort.objects.get(id=router_port_id)
        logger.info("获取路由器端口信息：{}".format(router_port))

        # 查询已分配的IP地址
        distribute_ports = Workstation.objects.filter(switch_id=switch_id).values_list("switch_port_id", flat=True)
        switch_ports = SwitchPort.objects.filter(id__in=distribute_ports)
        assign_ips = [ipaddress.IPv4Address(item.ip_addr) for item in switch_ports]
        logger.info("已分配的IP地址：{}".format(assign_ips))

        start_addr = ipaddress.IPv4Address(router_port.start_addr)
        end_addr = ipaddress.IPv4Address(router_port.end_addr)
        mask = router_port.mask
        gateway = router_port.gateway
        dns = router_port.dns
        logger.info("路由器端口信息：start_addr={}, end_addr={}, mask={}, gateway={}, dns={}".format(start_addr, end_addr, mask, gateway, dns))

        # 找出未分配的最小IP地址
        distribute_ip = None
        for ip_int in range(int(start_addr), int(end_addr) + 1):
            if ipaddress.IPv4Address(ip_int) not in assign_ips:
                distribute_ip = ipaddress.IPv4Address(ip_int)
                break
        if not distribute_ip:
            raise BusinessException("所有IP地址均已分配")
        data = {
            "ip_addr": str(distribute_ip),
            "dns": dns,
            "gateway": gateway,
            "mask": mask,
        }
        logger.info("分配地址：{}".format(data))
        return data
