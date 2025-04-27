from rest_framework import serializers

from ip_distribution.utils.constants_util import DesignerApplicationStatus
from distribution.models import User


class RegisterSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=64, required=True, help_text="用户名")
    password = serializers.CharField(max_length=32, required=True, help_text="密码")
    confirm_password = serializers.CharField(max_length=32, required=True, help_text="确认密码")
    gender = serializers.ChoiceField(choices=[(1, "男"), (0, "女")], help_text="1男，0女")
    phone = serializers.CharField(max_length=32, required=True, help_text="手机号")
    nickname = serializers.CharField(max_length=64, required=True, help_text="昵称")


class UserModifySerializer(serializers.Serializer):

    username = serializers.CharField(max_length=64, required=False, help_text="用户名")
    gender = serializers.ChoiceField(choices=[(1, "男"), (0, "女")], help_text="1男，0女")
    phone = serializers.CharField(max_length=32, required=False, help_text="手机号")
    nickname = serializers.CharField(max_length=64, required=True, help_text="昵称")


class ApplyAsDesignerSerializer(serializers.Serializer):

    reason = serializers.CharField(max_length=512, required=True, help_text="申请理由")


class RechargeSerializer(serializers.Serializer):

    amount = serializers.FloatField(required=True, help_text="充值金额")


class ApproveDesignerApplicationSerializer(serializers.Serializer):

    status = serializers.ChoiceField(choices=[
        (DesignerApplicationStatus.PASS.value, "通过"),
        (DesignerApplicationStatus.REFUSE.value, "拒绝")
    ], required=True)
    approval_opinions = serializers.CharField(max_length=512, required=False)
    record_id = serializers.IntegerField(required=True)


class PublishDraftSerializer(serializers.Serializer):

    title = serializers.CharField(max_length=512, required=False)
    description = serializers.CharField(max_length=512, required=False)
    image = serializers.FileField(required=True)
    price = serializers.FloatField(required=True)
    category_id = serializers.IntegerField(required=True)


class CreateOrderSerializer(serializers.Serializer):

    draft_id = serializers.IntegerField(required=True)


class OrderDeleteSerializer(serializers.Serializer):

    order_id = serializers.IntegerField(required=True)


class UserDeleteSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=64, required=True)
