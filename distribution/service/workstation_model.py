import time

from django.core.paginator import Paginator
from django.forms import model_to_dict

from distribution.models import Router, RouterPort, Switch, Workstation, SwitchPort
from ip_distribution.utils.exception_util import BusinessException
from ip_distribution.utils.log_util import get_logger

logger = get_logger("workstation")


class WorkstationModel(object):

    def add(self, code, switch_port_id, location):
        add_params = {
            "code": code,
            "switch_port_id": switch_port_id,
            "location": location,
        }
        logger.info("添加工位信息：{}".format(add_params))
        Switch.objects.create(**add_params)
        logger.info("添加工位成功：{}".format(add_params))

    def detail(self, workstation_id):
        workstation = Workstation.objects.get(id=workstation_id)
        workstation_info = model_to_dict(workstation)

        switch_port = SwitchPort.objects.get(id=workstation.switch_port_id)
        switch = Switch.objects.get(id=switch_port.switch_id)

        workstation_info["switch_name"] = switch.name
        workstation_info["ip_addr"] = switch_port.ip_addr
        workstation_info["dns"] = switch_port.dns
        workstation_info["mask"] = switch_port.mask
        workstation_info["gateway"] = switch_port.gateway
        return workstation_info

    def modify(self, work_station_id, code, switch_port_id, location):
        modify_params = {}
        if code:
            modify_params["code"] = code
        if switch_port_id:
            modify_params["switch_port_id"] = switch_port_id
        if location:
            modify_params["location"] = location
        logger.info("修改交换机信息：{}".format(modify_params))
        Workstation.objects.filter(id=work_station_id).update(**modify_params)

    def workstation_list(self, page, size, **kwargs):
        workstation_list = Workstation.objects.all().order_by("-id")
        if kwargs.get("code"):
            workstation_list = workstation_list.filter(code__icontains=kwargs.get("code"))
        if kwargs.get("location"):
            workstation_list = workstation_list.filter(location__icontains=kwargs.get("location"))

        switch_map = {}
        switch_list = Switch.objects.all()
        for item in switch_list:
            switch_map[item.id] = item.name
        switch_port_map = {}
        switch_port_list = SwitchPort.objects.all()
        for item in switch_port_list:
            switch_port_map[item.id] = model_to_dict(item)

        count = workstation_list.count()
        paginator = Paginator(workstation_list, size)
        workstation_list = paginator.get_page(page)
        data_list = []
        for item in workstation_list:
            obj = model_to_dict(item)
            switch_port = switch_port_map.get(obj.get("switch_port_id"))

            obj["switch_name"] = switch_map.get(obj.get("switch_id"))
            obj["ip_addr"] = switch_port.get("ip_addr")
            obj["dns"] = switch_port.get("dns")
            obj["gateway"] = switch_port.get("gateway")
            obj["mask"] = switch_port.get("mask")

        return {"count": count, "list": data_list}

    def del_workstation(self, workstation_id):
        workstation = Workstation.objects.get(id=workstation_id)
        workstation.delete()
        logger.info("已删除工位：{}".format(workstation))

