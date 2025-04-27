from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    id = models.BigAutoField(primary_key=True)
    nickname = models.CharField(max_length=64, null=True)
    gender = models.IntegerField(default=0, null=True)
    phone = models.CharField(max_length=32, null=True)
    is_ban = models.IntegerField(default=0)
    role = models.CharField(max_length=20)
    balance = models.FloatField(default=0.00)

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.username

class WalletOrder(models.Model):
    """钱包充值订单表"""

    id = models.BigAutoField(primary_key=True)
    order_uuid = models.CharField(max_length=36)
    user_id = models.BigIntegerField()
    status = models.CharField(max_length=20)
    amount = models.FloatField()
    seller_id = models.CharField(max_length=64)
    buyer_id = models.CharField(max_length=64)
    create_time = models.BigIntegerField()
    received_time = models.BigIntegerField()

    class Meta:
        db_table = 'wallet_order'


class Order(models.Model):
    """购买画稿订单表"""

    id = models.BigAutoField(primary_key=True)
    order_uuid = models.CharField(max_length=64)
    user_id = models.BigIntegerField()
    amount = models.FloatField()
    status = models.CharField(max_length=20)
    draft_id = models.BigIntegerField()
    create_time = models.BigIntegerField()
    is_cancel = models.IntegerField()
    cancel_time = models.BigIntegerField()

    class Meta:
        db_table = 'order'


class Category(models.Model):

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=1024)


class Draft(models.Model):

    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=1024)
    image_name = models.CharField(max_length=128)
    image_url = models.CharField(max_length=2048)
    price = models.FloatField()
    category_id = models.BigIntegerField()
    designer_id = models.BigIntegerField()
    status = models.CharField(max_length=20)
    online_time = models.BigIntegerField()
    is_outline = models.IntegerField(default=0)

    class Meta:
        db_table = 'ip_distribution'


class Browse(models.Model):

    id = models.BigAutoField(primary_key=True)
    user_id = models.BigIntegerField()
    draft_id = models.BigIntegerField()

    class Meta:
        db_table = 'browse'


class Crawler(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=1024)
    image_path = models.CharField(max_length=2048)

    class Meta:
        db_table = 'crawler'


class DesignerApplicationRecord(models.Model):

    id = models.BigAutoField(primary_key=True)
    user_id = models.BigIntegerField()
    reason = models.CharField(max_length=256)
    status = models.CharField(max_length=20)
    approval_opinions = models.CharField(max_length=256)
    approval_time = models.BigIntegerField()
    create_time = models.BigIntegerField()

    class Meta:
        db_table = 'designer_application_record'
