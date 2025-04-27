from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    id = models.BigAutoField(primary_key=True)
    nickname = models.CharField(max_length=64, null=True)
    gender = models.IntegerField(default=0, null=True)
    phone = models.CharField(max_length=32, null=True)
    is_ban = models.IntegerField(default=0)
    role = models.CharField(max_length=20)
    department_id = models.IntegerField(null=True),
    workstation_id = models.IntegerField(null=True)

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.username


class Department(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="部门名称")
    code = models.CharField(max_length=50, verbose_name="部门编码")
    manager_id = models.IntegerField(null=True, verbose_name="部门负责人ID")

    class Meta:
        db_table = 'department'

    def __str__(self):
        return self.name


class Router(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="路由器名称")

    class Meta:
        db_table = 'router'

    def __str__(self):
        return self.name


class RouterPort(models.Model):
    id = models.BigAutoField(primary_key=True)
    router_id = models.IntegerField(null=True, verbose_name="所属路由器ID")
    code = models.IntegerField(verbose_name="端口编号")
    dns = models.CharField(max_length=50, verbose_name="DNS地址")
    network_segment = models.CharField(max_length=50, verbose_name="网段")
    gateway = models.CharField(max_length=50, verbose_name="网关地址")

    class Meta:
        db_table = 'router_port'

    def __str__(self):
        return self.code


class Switch(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="交换机名称")
    code = models.CharField(max_length=50, verbose_name="交换机编码")
    router_port_id = models.IntegerField(null=True, verbose_name="关联路由器端口ID")
    department_id = models.IntegerField(null=True, verbose_name="所属部门ID")

    class Meta:
        db_table = 'switch'

    def __str__(self):
        return self.name


class SwitchPort(models.Model):
    id = models.BigAutoField(primary_key=True)
    switch_id = models.IntegerField(null=True, verbose_name="所属交换机ID")
    code = models.IntegerField(verbose_name="端口编号")
    ip_addr = models.CharField(max_length=50, null=True, blank=True, verbose_name="IP地址")

    class Meta:
        db_table = 'switch_port'


class Workstation(models.Model):
    id = models.BigAutoField(primary_key=True)
    code = models.CharField(max_length=50, verbose_name="工位编码")
    department_id = models.IntegerField(null=True, verbose_name="所属部门ID")
    switch_port_id = models.IntegerField(null=True, verbose_name="关联交换机端口ID")

    class Meta:
        db_table = 'workstation'

    def __str__(self):
        return self.code
