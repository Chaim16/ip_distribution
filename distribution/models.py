from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    id = models.BigAutoField(primary_key=True)
    nickname = models.CharField(max_length=64, null=True)
    gender = models.IntegerField(default=0, null=True)
    phone = models.CharField(max_length=32, null=True)
    is_ban = models.IntegerField(default=0)
    role = models.CharField(max_length=20)

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.username


class Router(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="路由器名称")
    model = models.CharField(max_length=255, verbose_name="型号")
    location = models.CharField(max_length=255, verbose_name="位置")
    port_num = models.IntegerField(verbose_name="端口数量")
    create_time = models.BigIntegerField(verbose_name="创建时间")
    create_user = models.CharField(max_length=255, verbose_name="创建人")

    class Meta:
        db_table = 'router'

    def __str__(self):
        return self.name


class RouterPort(models.Model):
    id = models.BigAutoField(primary_key=True)
    code = models.CharField(max_length=50, verbose_name="端口编号")
    router_id = models.IntegerField(null=True, verbose_name="所属路由器ID")
    start_addr = models.CharField(max_length=50, verbose_name="起始IP地址")
    end_addr = models.CharField(max_length=50, verbose_name="结束IP地址")
    mask = models.CharField(max_length=50, verbose_name="子网掩码")
    gateway = models.CharField(max_length=50, verbose_name="网关地址")
    dns = models.CharField(max_length=50, verbose_name="DNS地址")
    create_time = models.BigIntegerField(verbose_name="创建时间")
    create_user = models.CharField(max_length=50, verbose_name="创建人")

    class Meta:
        db_table = 'router_port'

    def __str__(self):
        return self.code


class Switch(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="交换机名称")
    code = models.CharField(max_length=50, verbose_name="交换机编码")
    model = models.CharField(max_length=255, verbose_name="型号")
    location = models.CharField(max_length=255, verbose_name="位置")
    router_id = models.IntegerField(null=True, verbose_name="关联路由器ID")
    router_port_id = models.IntegerField(null=True, verbose_name="关联路由器端口ID")
    port_num = models.IntegerField(verbose_name="端口数量")
    create_time = models.BigIntegerField(verbose_name="创建时间")
    create_user = models.CharField(max_length=255, verbose_name="创建人")

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
    location = models.CharField(max_length=255, verbose_name="位置")
    switch_id = models.IntegerField(null=True, verbose_name="关联交换机ID")
    switch_port_id = models.IntegerField(null=True, verbose_name="关联交换机端口ID")
    user_id = models.IntegerField(null=True, verbose_name="关联用户ID")

    class Meta:
        db_table = 'workstation'

    def __str__(self):
        return self.code
